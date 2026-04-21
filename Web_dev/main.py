from flask import Flask, render_template, request, session
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'I_love_India'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'hr_erp_db'

mysql = MySQL(app)


@app.route('/')
def home_page():
    return render_template('home.html')


@app.route('/contact')
def contact_page():
    return render_template('contact.html')
@app.route('/about')
def about_page():
    return render_template('about.html')

@app.route('/admin')
def admin_page():
    return render_template('admin.html')


@app.route('/admindashboard', methods=['POST'])
def admindashboard():
    user=request.form['txtUsername']
    passw=request.form['txtPassword']

    if user=='Ajit' and passw=='root':
        session['name']=user
        return render_template('admin_dashboard.html')
    else:
        msg='Invalid Username and Password'
        return render_template('admin.html', massage=msg)






@app.route('/addemployee')
def addemployee_page():
    return render_template('add_employee.html')

@app.route('/showemployee')
def showemployee_page():
    cur=mysql.connection.cursor()

    cur.execute('select empid, empname, empemail, mobile, designation, salary from registration')
    plist =cur.fetchall()
    cur.close()
    return render_template('show_employee_detail.html', recordlist=plist)

@app.route('/admin_emp_profile')
def admin_emp_profile_page():
    id=request.args.get('empid')
    cur=mysql.connection.cursor()
    cur.execute('select * from registration where empid='+ id)
    plist=cur.fetchall()
    return render_template('admin_emp_profile.html', recordlist=plist)





@app.route('/save', methods=['POST'])
def save_page():
    i= request.form['txtId']
    n= request.form['txtName']
    e= request.form['txtEmail']
    m=request.form['txtMobile']
    d= request.form['txtDesignation']
    s=request.form['txtSalary']

    cur=mysql.connection.cursor()

    cur.execute('insert into registration (empid, empname, empemail, mobile, designation, salary) values(%s,%s,%s,%s,%s,%s)',(i,n,e,m,d,s))

    mysql.connection.commit()
    cur.close()

    return render_template('admin_reg_success.html')


@app.route('/admin_emp_update', methods=['POST'])
def admin_emp_update_page():
    i = request.form['txtId']
    n = request.form['txtName']
    e = request.form['txtEmail']
    m = request.form['txtMobile']
    d = request.form['txtDesignation']
    s = request.form['txtSalary']

    cur=mysql.connection.cursor()
    cur.execute('update registration set empname=%s, designation=%s, mobile=%s, empemail=%s, salary=%s where empid=%s ',(n,d,m,e,s, i,))
    mysql.connection.commit()
    cur.close()
    return render_template('admin_emp_updated_record.html')

@app.route('/admin_emp_delete')
def admin_emp_delete_page():
    id=request.args.get('empid')
    cur=mysql.connection.cursor()
    cur.execute('delete from registration where empid=%s ',(id,))
    mysql.connection.commit()
    plist=cur.fetchall()
    return render_template('admin_emp_delete_record.html', recordlist=plist )

@app.route('/searchemployee')
def searchemployee_page():
    return render_template('admin_searchemployee.html')

@app.route('/search_result', methods=['POST'])
def search_result_page():
   i= request.form['txtId']

   cur=mysql.connection.cursor()
   cur.execute('select * from registration where empid=%s',(i, ))

   plist=cur.fetchall()
   cur.close()
   return render_template('search_result.html', recordlist=plist)


@app.route('/logout')
def logout():
    session['name']=None
    return render_template('admin.html')

app.run(debug=True)
