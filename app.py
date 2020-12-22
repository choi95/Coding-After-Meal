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
    import pandas as pd
    try:
        cur = mysql.connection.cursor()
        cur.execute("select * from food_information")
        info = cur.fetchall()
    except Exception as e:
        print('cur error:', e)
    result = pd.DataFrame(info)
    print(result)
    value = []
    value.append(int(request.args.get('a')))
    value.append(int(request.args.get('b')))
    value.append(int(request.args.get('c')))
    value.append(int(request.args.get('d')))
    value.append(int(request.args.get('e')))
    value.append(int(request.args.get('f')))
    print(value)
    # stress
    for i in range(62):
        if result.loc[i, 11] != value[1]:
            result = result.drop(i)
    result=result.reset_index(drop=True)

    # 다이어트
    size = len(result)
    height = 160
    for i in range(size):
        recommended_calories = (height - 100) * 0.9 * 30
        if value[2] == 1:
            cal = recommended_calories * (2 / 5) - 200

        if value[2] == 2:
            cal = recommended_calories * (2 / 5)

        if value[2] == 3:
            cal = recommended_calories * (2 / 5) + 200

    for i in range(size):
        if result.loc[i, 5] > cal:
            result = result.drop(index=i)
    result = result.reset_index(drop=True)

    # 오늘 날씨 어때요?
    size = len(result)
    for i in range(size):
        if value[3] == 3 and result.loc[i, 4] < 2:
            result = result.drop(index=i)
    result = result.reset_index(drop=True)

    # 가격대
    size = len(result)
    for i in range(size):
        if value[4] == 1:
            if result.loc[i, 2] < 2000 and result.loc[i, 2] > 3000:
                result = result.drop(index=i)
        if value[4] == 2:
            if result.loc[i, 2] < 3000 and result.loc[i, 2] > 4000:
                result = result.drop(index=i)
        if value[4] == 3:
            if result.loc[i, 2] < 4000 and result.loc[i, 2] > 5000:
                result = result.drop(index=i)
    result = result.reset_index(drop=True)
    print(result)

    result = [result[1][0],result[1][1],result[1][2]]

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
