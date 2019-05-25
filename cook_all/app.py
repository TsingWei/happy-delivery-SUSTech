from flask import Flask, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap
from flask_bootstrap import WebCDN
from flask_login import LoginManager, login_user, login_required,logout_user,current_user
from cook_all.adapter import dishadapter
from cook_all.bean.user import Cook
from cook_all.bean.user import query_user
from cook_all.dao.ChefToDish import ChefToDish
from cook_all.adapter import Commentadapter
from cook_all.dao.Dish import Dish

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
dishes = []


# 测试页面
@app.route('/test')
def test():
    return render_template('base.html')

@app.route('/', methods=['GET', 'POST'])
@login_required
def hello_world():  # 登陆后首页,点餐页面
    # form = myForm.OrderForm()
    global dishes
    dishid = request.form.get('dishid')
    current_user.curr_order[dishid] = 1
    # print(request.form.get('add_dish'))
    if request.form.get('see_comment'):
        return comments(dishid)
    if dishid is not None and request.form.get('add_dish') is not None:
        ChefToDish.modify_remain(current_user.chef_id, int(dishid), 1)
    if current_user.chef_id is not None:
        dishes = dishadapter.getalldish(chefid=current_user.chef_id)
    return render_template('home.html', dishes=dishes)


@app.route('/home.html', methods=['GET', 'POST'])
@login_required
def logout():
    # logout_user()
    logout_user()
    return render_template('login.html')


@app.route('/comments', methods=['GET'])
@login_required
def comments(dishid):
    # comments = get_comments(dish_id, current_user.id)
    dishid = request.form.get('see_comment')
    print("dishid:" + str(dishid))
    comment = Commentadapter.getallcomment(dishid, current_user.chef_id)
    dish_name = Dish.find_dish(int(dishid))[0]['dish_name']
    return render_template('commets.html', comments=comment, dish_name=dish_name)


@app.route('/login', methods=['GET', 'POST'])
def login():  # 登录页面
    if request.method == 'POST':
        chefid = request.form.get('username')
        print("username: " + chefid)
        global dishes
        dishes = dishadapter.getalldish(chefid=int(chefid))
        user = query_user(chefid)

        # 验证表单中提交的用户名和密码
        if user is not None:
            curr_user = Cook()
            curr_user.id = chefid

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
def load_user(chefid):
    res = query_user(int(chefid))
    if res is not None:
        curr_user = Cook(res[0])
        curr_user.id = chefid
        return curr_user
    else:
        return None


if __name__ == '__main__':
    app.run()
