from flask import Flask, render_template, url_for, request, redirect
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)

db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

@app.errorhandler(404)
def page_not_found(error):
    app.logger.error(error)
    return render_template('page_not_found.html'), 404

@app.route('/', methods=['GET', 'POST'])
def method():
    try:
        cur = mysql.connection.cursor()
        cur.execute("CREATE TABLE users(Username varchar(50), Age varchar(50), Gender varchar(50), Height varchar(50), Weight varchar(50))") 
        mysql.connection.commit()
    except Exception as e:
        print('cur error:', e)
    if request.method=='POST':
        # Fetch form data
        print('POST')
        userDetails = request.form
        Username = userDetails['Username']
        Age = userDetails['Age']
        Gender = userDetails['Gender']
        Height = userDetails['Height']
        Weight = userDetails['Weight']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(Username, Age, Gender, Height, Weight) VALUES(%s, %s, %s, %s, %s)",(Username, Age, Gender, Height, Weight))
        mysql.connection.commit()
        cur.close()
        return redirect("/select/")

    else:
        print("GET")
        return render_template('login.html')
    return 'BACK'

@app.route('/users')
def users():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM users")
    if resultValue > 0:
        userDetails = cur.fetchall()
        return render_template('users.html',userDetails=userDetails)
    return 'miss'

@app.route('/removeAll')
def remove():
    #table을 삭제하여 완전히 초기화한다.
    cur = mysql.connection.cursor()
    cur.execute("DROP TABLE users")
    return 'removeALL'

@app.route('/home/')
def home():
    return render_template('home.html', title="hello jinja")


@app.route('/page1/', methods=['GET'])
def page1():
    a = request.args.get('a')
    result = ["떡볶이","햄버거",a]
    return render_template('page1.html',menu = result)


@app.route('/page2/')
def page2():
    return render_template('page2.html')

@app.route('/index/')
def index():
    return render_template('index.html')


@app.route('/select/')
def select():
    return render_template('select.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
