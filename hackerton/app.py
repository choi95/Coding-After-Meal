from flask import Flask, render_template,url_for

app = Flask(__name__)

@app.errorhandler(404)
def page_not_found(error):
    app.logger.error(error)
    return render_template('page_not_found.html'), 404
@app.route('/home/')
def home():
    return render_template('home.html',title="hello jinja")
@app.route('/page1/')
def page1():
    return render_template('page1.html')
@app.route('/index/')
def index():
    return render_template('index.html')
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)



