from flask import Flask, render_template, redirect, url_for
from AzureDB import AzureDB
from flask_dance.contrib.github import make_github_blueprint, github
import secrets
import os

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

github_blueprint = make_github_blueprint(
    client_id="818a9e110420c482eb69",
    client_secret="91ee0a85d576d15600e21a3f8e7a5ee084722b56"
)
app.register_blueprint(github_blueprint, url_prefix='/login')


@app.route('/')
def index():
    if not github.authorized:
        return redirect(url_for('github.login'))
    else:
        account_info = github.get('/user')
        if account_info.ok:
            account_info_json = account_info.json()
            return render_template('index.html')
    return '<h1>Request failed!</h1>'


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/gallery')
def gallery():
    return render_template('gallery.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/guestbook')
def guestbook():
    with AzureDB() as a:
        data = a.azureGetData()
    return render_template("guestbook.html", data = data)


if __name__ == '__main__':
    app.run(debug=True)
