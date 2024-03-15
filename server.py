import yaml
from flask import Flask, render_template, request,redirect
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configure the db
db = yaml.safe_load(open('db.yaml'))
app.config['MYSQL_HOST']=db['mysql_host']
app.config['MYSQL_USER']=db['mysql_user']
app.config['MYSQL_PASSWORD']=db['mysql_password']
app.config['MYSQL_DB'] =db['mysql_db']

# pass this app as an instance to MYSQL
mysql = MySQL(app)
@app.route("/home")
def home2():
    return render_template('home.html')
@app.route("/index")
def index():
    return render_template('index.html')
@app.route("/")
def home():
    return render_template('home.html')
@app.route("/form",methods=['GET','POST'])
def form():
    if request.method=='POST':
        userDetail = request.form
        # id = userDetail['id']
        name = userDetail['name']
        email = userDetail['email']
        Mobile = userDetail['Mobile']
        visit_date = userDetail['visit_date']
        cur = mysql.connection.cursor()
        cur.execute("insert into visitor(name,email,Mobile,visit_date) values(%s,%s,%s,%s)",(name,email,Mobile,visit_date))
        mysql.connection.commit()
        cur.close()
        return 'success '
        return redirect('/userdetails')
    return render_template('form.html')
@app.route('/userdetails')
def userdetails():
    # first step is to make a database cursor
    cur = mysql.connection.cursor()
    resultValue = cur.execute(" select * from visitor")
    if resultValue>=0:
        userDetail = cur.fetchall()
        return render_template('details.html',userDetail = userDetail)


@app.route("/delete",methods=['GET','POST'])
def delete():
    if request.method=='POST':
        delDetail = request.form
        idd = delDetail['id']
        cur = mysql.connection.cursor()
        sql = "delete from visitor where id = %s"
        adr = (idd,)
        cur.execute(sql, adr)
        mysql.connection.commit()
        cur.close()
        return 'record deleted'
    return render_template('delete.html')

@app.route("/update",methods=['GET','POST'])
def update():
    if request.method=='POST':
        userDetail = request.form
        id = userDetail['id']
        name = userDetail['name']
        email = userDetail['email']
        Mobile = userDetail['Mobile']
        visit_date = userDetail['visit_date']
        cur = mysql.connection.cursor()
        cur.execute("update visitor set name=%s,email=%s,Mobile=%s,visit_date=%s where id=%s",(name,email,Mobile,visit_date,id))
        mysql.connection.commit()
        cur.close()
        return 'update successfully '

    return render_template('/update.html')




if __name__=='__main__':
    app.run(debug=True)
