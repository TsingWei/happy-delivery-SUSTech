from flask import Flask, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap
from flask_bootstrap import WebCDN
from flask_login import LoginManager, login_user, login_required,logout_user,current_user

# import bean.dish as dish
from delivery_all.bean.user import User
from delivery_all.bean.user import query_user
from delivery_all.adapter import dishAdapter

login_manager = LoginManager()
app = Flask(__name__)
bootstrap = Bootstrap(app)
login_manager.init_app(app)
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'

app.extensions['bootstrap']['cdns']['jquery'] = WebCDN(
    '//cdnjs.cloudflare.com/ajax/libs/jquery/4.6.0/'
)

app.secret_key = '11111111'  # CSRF密钥
curr_order = {}

# 测试页面
@app.route('/test')
def test():
    return render_template('base.html')

@app.route('/', methods=['GET', 'POST'])
@login_required
def hello_world():  # 登陆后首页,点餐页面
    global curr_order

    # form = myForm.OrderForm()
    dishID = request.form.get('dishname')
    hallID = request.args.get('hall')
    if hallID is None:
        hallID = 1

    print('hall ID is ', hallID)
    dishes = dishAdapter.getalldish(hallID)
    print(dishID)
    if dishID in curr_order:
        curr_order[dishID] += 1
    else:
        curr_order[dishID] = 1
    current_user.curr_order = curr_order
    return render_template('home.html', dishes=dishes)


@app.route('/home.html', methods=['GET', 'POST'])
@login_required
def logout():
    # logout_user()
    logout_user()
    return render_template('login.html')

@app.route('/order_done', methods=['GET', 'POST'])
@login_required
def order_done():
    curr_order.clear()
    return('下单成功!')

@app.route('/login', methods=['GET', 'POST'])
def login():  # 登录页面
    if request.method == 'POST':
        username = request.form.get('username')
        print(username)
        user = query_user(username)

        # 验证表单中提交的用户名和密码
        if user is not None:
            curr_user = User()
            curr_user.id = username

            # 通过Flask-Login的login_user方法登录用户
            login_user(curr_user)

            # 如果请求中有next参数，则重定向到其指定的地址，
            # 没有next参数，则重定向到"index"视图
            next = request.args.get('next')
            return redirect(next or url_for('hello_world'))

        flash(u'用户名错误!', 'error')
        # GET 请求
    return render_template('login.html')


# 如果用户名存在则构建一个新的用户类对象，并使用用户名作为ID
# 如果不存在，必须返回None
@login_manager.user_loader
def load_user(user_id):
    res = query_user(int(user_id))
    if res is not None:
        curr_user = User(res[0])
        curr_user.id = user_id
        return curr_user
    else:
        return None


if __name__ == '__main__':
    app.run()
