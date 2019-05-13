from flask import Flask, request, render_template
from flask_bootstrap import Bootstrap
from flask_bootstrap import WebCDN

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.extensions['bootstrap']['cdns']['jquery'] = WebCDN(
    '//cdnjs.cloudflare.com/ajax/libs/jquery/4.6.0/'
)

@app.route('/test')
def test():
    return render_template('base.html')

@app.route('/')
def hello_world():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

if __name__ == '__main__':
    app.run()
