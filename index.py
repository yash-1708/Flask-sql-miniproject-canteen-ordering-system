from flask import Flask,render_template,request,flash,url_for,redirect
import mysql.connector
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired,Length

app=Flask(__name__)

app.config['SECRET_KEY']='b4c4f4b70ec9b4e0'

@app.route('/',methods=['GET', 'POST'])
@app.route('/home')
def home():
    try:
        cnx = mysql.connector.connect(user="root", password='yash', host="127.0.0.1", port=3306, database='canteendb')
        mycursor = cnx.cursor()
        sqlquery = "SELECT * FROM menu_master"
        mycursor.execute(sqlquery)
        data = mycursor.fetchall()
        title = "MENU"
        
        return render_template('/home.html', output_data = data, titletext = title)
    except mysql.connector.Error as err:
        if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        else:
            print(err)

class RecordEnterForm(FlaskForm):
    item_code=StringField('Order Details ',validators=[DataRequired(),Length(min=1)])
    submit=SubmitField('Submit')

#Order function
@app.route('/order',methods=['GET', 'POST'])
def enterRecommendation():
    form=RecordEnterForm(request.form)
    if request.method == 'POST':
        item_code=request.form['item_code']
        student_name=request.form['student_name']
        print("******Ordered ",item_code,"******")

        if form.validate():
            try:
                cnx = mysql.connector.connect(user="root", password='yash', host="127.0.0.1", port=3306, database='canteendb')        
                mycursor = cnx.cursor()
                
                orderinsertquery = "INSERT INTO order_master(item_code, student_name, date) VALUES ("+item_code+", '"+student_name+"', CURDATE());"
                mycursor.execute(orderinsertquery)
                cnx.commit()
                flash('Order Complete!')
            except mysql.connector.Error as err:
                if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
                    print("Something is wrong with your user name or password")
                    flash('Order Invalid!')
                else:
                    print(err)
                    flash('Order Invalid!')            
        else:
            flash('Error: occurred ')
    return render_template('/recordEnter.html',form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('adminhome'))
    return render_template('login.html', error=error)

@app.route('/adminhome',methods=['GET', 'POST'])
def adminhome():

    try:
        cnx = mysql.connector.connect(user="root", password='yash', host="127.0.0.1", port=3306, database='canteendb')
        mycursor = cnx.cursor()
        sqlquery = "SELECT * FROM canteendb.order_master INNER JOIN canteendb.menu_master ON order_master.item_code = menu_master.item_code;"
        mycursor.execute(sqlquery)
        data = mycursor.fetchall()
        title = "ORDERS FOR THE DAY"
        
        if 'clear_button' in request.form :
            sqlquery1 = "TRUNCATE TABLE order_master;"
            mycursor.execute(sqlquery1)
        return render_template('/adminhome.html', output_data = data, titletext = title)

        
    except mysql.connector.Error as err:
        if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        else:
            print(err)

#Below line code is necessary for running file as python index.py
if __name__=='__main__':
    app.run(debug=True)
