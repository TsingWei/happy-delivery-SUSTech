from flask import Flask, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap
from flask_bootstrap import WebCDN
from flask_login import LoginManager, login_user, login_required,logout_user,current_user

# import bean.dish as dish
from user_all.bean.user import User
from user_all.bean.user import query_user
from user_all.adapter import dishAdapter
from user_all.dao.Address import Address
from user_all.dao.Order import Order

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
curr_order_id = {}
hallID = None

# 测试页面
@app.route('/test')
def test():
    return render_template('user_all/templates/base.html')

@app.route('/', methods=['GET', 'POST'])
@login_required
def hello_world():  # 登陆后首页,点餐页面
    global curr_order,hallID,curr_order_id

    # form = myForm.OrderForm()
    dishname = request.form.get('dishname')
    dishID = request.form.get('dishid')
    hallID = request.args.get('hall')
    if hallID is None:
        hallID = 1
    else:
        hallID = int(hallID)
    if dishID is not None:
        dishID = int(dishID)
    print('hall ID is ', hallID)
    dishes = dishAdapter.getAlldish(hallID)
    print(dishname)

    if dishname in curr_order:
        curr_order[dishname] += 1
        curr_order_id[dishID] += 1
    elif dishname is not None:
        curr_order[dishname] = 1
        curr_order_id[dishID] = 1
    current_user.curr_order = curr_order
    return render_template('home.html', dishes=dishes)


@app.route('/home.html', methods=['GET', 'POST'])
@login_required
def logout():
    # logout_user()
    curr_order.clear()
    curr_order_id.clear()
    logout_user()
    return render_template('login.html')

@app.route('/order_done', methods=['GET', 'POST'])
@login_required
def order_done():
    id = current_user.user_id
    addresses = Address.find_address(uid=int(id))
    print(addresses)
    current_user.curr_order = curr_order
    # curr_order.clear()
    return render_template('order_done.html', addresses=addresses)



@app.route('/done', methods=['GET', 'POST'])
@login_required
def done():
    global hallID
    if request.method == 'POST':
        address_id = request.form.get('address_id')
        print('jjjjjjjj',curr_order_id)
        state = 'NC'
        hall_id = int(hallID)
        Order.new_order(int(address_id),state,curr_order_id,hall_id)
        curr_order.clear()
        curr_order_id.clear()
        # curr_order.clear()
        return redirect(url_for('hello_world'))

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
