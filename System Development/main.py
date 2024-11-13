

import pymysql
import os
import json
from datetime import datetime
import datetime as dt
from flask import Flask, render_template, session, request, redirect, url_for ,flash
import mysql.connector
from pdf_processing.upload_pdf import upload_pdf  # 导入 upload_pdf 函数
from dash_app.plot_functions import map
from dash_app import create_dash_app
import callbacks
from dash import Input, Output
from scr.A_main import main

app = Flask(__name__)
app.secret_key = 'ESG'  # 用于会话管理

dash_app = create_dash_app(app)
# 数据库连接配置

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'a12345678',
    'database': 'esg_database',
    'charset': 'utf8mb4'
}




# 主页面：选择登录类型
@app.route('/')
def home():
    return render_template('index.html')

# importance
@app.route('/importance')
def importance():
    return render_template('Importance.html')


# Person 用户登录

@app.route('/login_person', methods=['GET', 'POST'])
def login_person():
    if request.method == 'POST':
        username = request.form.get('username')

        password = request.form.get('password')
        role = 'person'
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        query = """
                        SELECT * FROM User
                        WHERE user_name = %s AND password = %s AND role = %s
                    """
        cursor.execute(query, (username, password, role))
        # 获取匹配的记录
        user = cursor.fetchone()  # 返回第一条匹配记录
        cursor.close()
        conn.close()
        if user:
            session['username'] = username
            session['password'] = password
            session['role'] = role
            return redirect(url_for('dashboard'))
        else:
            login_massage = "Tips: The account or password is wrong"
            return render_template('Login-Person.html', message=login_massage)
    return render_template('Login-Person.html')


@app.route('/reset_password_person', methods=['GET', 'POST'])
def reset_password_person():
    if request.method == 'POST':
        role = 'person'
        username = request.form.get('username')
        phone_number = request.form.get('phone_number')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        query = """
                                SELECT * FROM User
                                WHERE user_name = %s AND phone_number = %s AND role = %s
                            """
        cursor.execute(query, (username, phone_number, role))
        if cursor.fetchone() is None:
            m1 = "Tips: Mobile phone number and user name do not correspond"
            return render_template('Reset-Password-Person.html', message=m1)
        else:
            if new_password == confirm_password:
                cursor.execute(
                    'UPDATE User SET password = %s WHERE user_name = %s AND role = %s',
                    (new_password, username, role)
                )
                conn.commit()
                return render_template('resetperson_success.html')

            else:
                m3 = "Tips: The password entered twice is inconsistent"
                return render_template('Reset-Password-Person.html', message=m3)
    return render_template('Reset-Password-Person.html')

@app.route('/register_person', methods=['GET', 'POST'])
def register_person():
    if request.method == 'POST':
        username = request.form.get('username')
        phone_number = request.form.get('phone_number')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # 检查两次密码是否一致
        if password != confirm_password:
            m1 = "Passwords do not match."
            return render_template('Register-Person.html', message=m1)

        else:
             # 插入新用户到数据库，并检查用户名唯一
            conn = pymysql.connect(**db_config)
            cursor = conn.cursor(pymysql.cursors.DictCursor)

            # 检查用户名是否已存在
            cursor.execute("SELECT * FROM User WHERE user_name = %s", (username,))
            if cursor.fetchone():
                message = "Username is already taken. Please choose another one."
                return render_template('Register-Person.html', message=message)
            else:
            # 插入用户数据，company_id = 0，role = 'person'

                role = 'person'
                query = """
                        INSERT INTO User (user_name, phone_number, password, role)
                        VALUES (%s, %s, %s, %s)
                    """
                cursor.execute(query,(username, phone_number, password,role))
                conn.commit()

            # 获取刚刚插入记录的 user_id
                user_id = cursor.lastrowid
                print("Generated user_id:", user_id)

                return render_template('registerperson_success.html')
    return render_template('Register-Person.html')

@app.route('/analysis_person', methods=['GET', 'POST'])
def analysis_person():
    if request.method == 'POST':
        # 获取用户选择的行业
        username = session['username']
        selected_industry = request.form.get('industry')
        session['industry'] = selected_industry
        firm_name = request.form.get('firmname')
        session["firm_name"] = firm_name
        stock_code = request.form.get("stockcode")
        session["stock_code"] = stock_code
        country = request.form.get('country')
        session["country"] = country
        website = request.form.get('website')
        session["website"] = website
        year = request.form.get('year')
        session["year"] = year
        file = request.files.get('pdf_file')
        print(file.filename)

        if file != '':
            main(username,selected_industry,firm_name,country,website,year,file)
            return redirect(url_for('uploadperson_success'))
        else:
            m3 = "There is a problem, please upload again."
            return render_template('Analysis-Person.html', message=m3)

    return render_template('Analysis-Person.html')

@app.route('/uploadperson_success', methods=['GET', 'POST'])
def uploadperson_success():

    return render_template('uploadperson_success.html')


@app.route('/report_person', methods=['GET', 'POST'])
def report_person():
    industry = session.get('industry', 'Unknown Industry')
    firm_name = session.get("firm_name", "Unknown Firm")
    stock_code = session.get("stock_code", "AAPL")  # 默认值
    country = session.get("country", "Unknown Country")
    website = session.get("website", "No Website Available")
    year = session.get("year", "No Year Provided")

    image_base64=map()
    return render_template(
        "Report-Person.html",
        industry=industry,
        firm_name=firm_name,
        stock_code=stock_code,
        country=country,
        website=website,
        year=year,
        image_base64=image_base64
    )


# Firm 用户登录

@app.route('/login_firm', methods=['GET', 'POST'])
def login_firm():
    if request.method == 'POST':
        username = request.form.get('username')

        password = request.form.get('password')
        role = 'firm'
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        query = """
                        SELECT * FROM User
                        WHERE user_name = %s AND password = %s AND role = %s
                    """
        cursor.execute(query, (username, password, role))
        # 获取匹配的记录
        user = cursor.fetchone()  # 返回第一条匹配记录
        cursor.close()
        conn.close()
        if user:
            session['username'] = username
            session['password'] = password
            session['role'] = role
            return redirect(url_for('dashboard'))
        else:
            login_massage = "Tips: The account or password is wrong"
            return render_template('Login-Firm.html', message=login_massage)
    return render_template('Login-Firm.html')


@app.route('/reset_password_firm', methods=['GET', 'POST'])
def reset_password_firm():
    if request.method == 'POST':
        role = 'firm'
        username = request.form.get('username')
        phone_number = request.form.get('phone_number')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        query = """
                                SELECT * FROM User
                                WHERE user_name = %s AND phone_number = %s AND role = %s
                            """
        cursor.execute(query, (username, phone_number, role))
        if cursor.fetchone() is None:
            m1 = "Tips: Mobile phone number and firm name do not correspond"
            return render_template('Reset-Password-Firm.html', message=m1)
        else:
            if new_password == confirm_password:
                cursor.execute(
                    'UPDATE User SET password = %s WHERE user_name = %s AND role = %s',
                    (new_password, username, role)
                )
                conn.commit()
                return render_template('resetfirm_success.html')

            else:
                m3 = "Tips: The password entered twice is inconsistent"
                return render_template('Reset-Password-Firm.html', message=m3)
    return render_template('Reset-Password-firm.html')

@app.route('/register_firm', methods=['GET', 'POST'])
def register_firm():
    if request.method == 'POST':
        username = request.form.get('username')
        phone_number = request.form.get('phone_number')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # 检查两次密码是否一致
        if password != confirm_password:
            m1 = "Passwords do not match."
            return render_template('Register-Firm.html', message=m1)

        else:
             # 插入新用户到数据库，并检查用户名唯一
            conn = pymysql.connect(**db_config)
            cursor = conn.cursor(pymysql.cursors.DictCursor)

            # 检查用户名是否已存在
            cursor.execute("SELECT * FROM User WHERE user_name = %s", (username,))
            if cursor.fetchone():
                message = "Username is already taken. Please choose another one."
                return render_template('Register-Firm.html', message=message)
            else:
            # 插入用户数据，company_id = 0，role = 'person'

                role = 'firm'
                query = """
                        INSERT INTO User (user_name, phone_number, password, role)
                        VALUES (%s, %s, %s, %s)
                    """
                cursor.execute(query,(username, phone_number, password, role))
                conn.commit()

            # 获取刚刚插入记录的 user_id
                user_id = cursor.lastrowid
                print("Generated user_id:", user_id)

                return render_template('registerfirm_success.html')
    return render_template('Register-Firm.html')

@app.route('/analysis_firm', methods=['GET', 'POST'])
def analysis_firm():
    if request.method == 'POST':
        # 获取用户选择的行业
        username = session['username']
        selected_industry = request.form.get('industry')
        session['industry'] = selected_industry
        firm_name = request.form.get('firmname')
        session["firm_name"] = firm_name
        stock_code = request.form.get("stockcode")
        session["stock_code"] = stock_code
        country = request.form.get('country')
        session["country"] = country
        website = request.form.get('website')
        session["website"] = website
        year = request.form.get('year')
        session["year"] = year
        file = request.files.get('pdf_file')
        print(file.filename)

        if file != '':
            main(username,selected_industry,firm_name,country,website,year,file)
            return render_template('uploadfirm_success.html')
        else:
            m3 = "There is a problem, please upload again."
            return render_template('Analysis-Firm.html', message=m3)

    return render_template('Analysis-Firm.html')

@app.route('/report_firm', methods=['GET', 'POST'])
def report_firm():
    industry = session.get('industry', 'Unknown Industry')
    firm_name = session.get("firm_name", "Unknown Firm")
    stock_code = session.get("stock_code", "AAPL")  # 默认值
    country = session.get("country", "Unknown Country")
    website = session.get("website", "No Website Available")
    year = session.get("year", "No Year Provided")
    image_base64=map()
    return render_template(
        "Report-Firm.html",
        industry=industry,
        firm_name=firm_name,
        stock_code=stock_code,
        country=country,
        website=website,
        year=year,
        image_base64=image_base64
    )



# Regulator 用户登录

@app.route('/login_regulator', methods=['GET', 'POST'])
def login_regulator():
    if request.method == 'POST':
        username = request.form.get('username')

        password = request.form.get('password')
        role = 'regulator'
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        query = """
                        SELECT * FROM User
                        WHERE user_name = %s AND password = %s AND role = %s
                    """
        cursor.execute(query, (username, password, role))
        # 获取匹配的记录
        user = cursor.fetchone()  # 返回第一条匹配记录
        cursor.close()
        conn.close()
        if user:
            session['username'] = username
            session['password'] = password
            session['role'] = role
            return redirect(url_for('dashboard'))
        else:
            login_massage = "Tips: The account or password is wrong"
            return render_template('Login-Regulator.html', message=login_massage)
    return render_template('Login-Regulator.html')


@app.route('/reset_password_regulator', methods=['GET', 'POST'])
def reset_password_regulator():
    if request.method == 'POST':
        role = 'regulator'
        username = request.form.get('username')
        phone_number = request.form.get('phone_number')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        query = """
                                SELECT * FROM User
                                WHERE user_name = %s AND phone_number = %s AND role = %s
                            """
        cursor.execute(query, (username, phone_number, role))
        if cursor.fetchone() is None:
            m1 = "Tips: Mobile phone number and user name do not correspond"
            return render_template('Reset-Password-Regulator.html', message=m1)
        else:
            if new_password == confirm_password:
                cursor.execute(
                    'UPDATE User SET password = %s WHERE user_name = %s AND role = %s',
                    (new_password, username, role)
                )
                conn.commit()
                return render_template('resetregulator_success.html')

            else:
                m3 = "Tips: The password entered twice is inconsistent"
                return render_template('Reset-Password-Regulator.html', message=m3)
    return render_template('Reset-Password-Regulator.html')

@app.route('/register_regulator', methods=['GET', 'POST'])
def register_regulator():
    if request.method == 'POST':
        username = request.form.get('username')
        phone_number = request.form.get('phone_number')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # 检查两次密码是否一致
        if password != confirm_password:
            m1 = "Passwords do not match."
            return render_template('Register-Firm.html', message=m1)

        else:
             # 插入新用户到数据库，并检查用户名唯一
            conn = pymysql.connect(**db_config)
            cursor = conn.cursor(pymysql.cursors.DictCursor)

            # 检查用户名是否已存在
            cursor.execute("SELECT * FROM User WHERE user_name = %s", (username,))
            if cursor.fetchone():
                message = "Username is already taken. Please choose another one."
                return render_template('Register-Regulator.html', message=message)
            else:
            # 插入用户数据，company_id = 0，role = 'person'

                role = 'regulator'
                query = """
                        INSERT INTO User (user_name, phone_number, password, role)
                        VALUES (%s, %s, %s, %s)
                    """
                cursor.execute(query,(username, phone_number, password, role))
                conn.commit()

            # 获取刚刚插入记录的 user_id
                user_id = cursor.lastrowid
                print("Generated user_id:", user_id)

                return render_template('registerregulator_success.html')
    return render_template('Register-Regulator.html')

@app.route('/analysis_regulator', methods=['GET', 'POST'])
def analysis_regulator():
    if request.method == 'POST':
        # 获取用户选择的行业
        username = session['username']
        selected_industry = request.form.get('industry')
        session['industry']=selected_industry
        firm_name= request.form.get('firmname')
        session["firm_name"] = firm_name
        stock_code=request.form.get("stockcode")
        session["stock_code"] = stock_code
        country=request.form.get('country')
        session["country"] = country
        website=request.form.get('website')
        session["website"] = website
        year= request.form.get('year')
        session["year"] = year
        file = request.files.get('pdf_file')
        print(file.filename)

        if file != '':
            main(username,selected_industry,firm_name,country,website,year,file)
            return render_template('uploadregulator_success.html')
        else:
            m3 = "There is a problem, please upload again."
            return render_template('Analysis-regulator.html', message=m3)

    return render_template('Analysis-regulator.html')

@app.route('/report_regulator', methods=['GET', 'POST'])
def report_regulator():
    industry = session.get('industry', 'Unknown Industry')
    firm_name = session.get("firm_name", "Unknown Firm")
    stock_code = session.get("stock_code", "AAPL")  # 默认值
    country = session.get("country", "Unknown Country")
    website = session.get("website", "No Website Available")
    year = session.get("year", "No Year Provided")
    image_base64=map()
    return render_template(
        "Report-Regulator.html",
        industry=industry,
        firm_name=firm_name,
        stock_code=stock_code,
        country=country,
        website=website,
        year=year,
        image_base64=image_base64
    )







# 登录后的仪表盘，根据角色重定向到不同的页面
@app.route('/dashboard')
def dashboard():
    if 'username' in session and 'role' in session:
        username = session['username']
        role = session['role']
        # 根据角色渲染不同的模
        if role == 'person':
            return render_template('Info-Person.html',username=username)
        elif role == 'firm':
            return render_template("Info-Firm.html", username=username, role=role)
        elif role == 'regulator':
            return render_template('Info-regulator.html', username=username, role=role)
    # 如果没有登录，重定向到主页
    return redirect(url_for('home'))

# 退出登录
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/about')
def about():
    return render_template("About.html")

@app.route('/help')
def help():
    return render_template("Help.html")

#  我的账户界面，可以修改密码，查看证件信息，可以链接到注销和退出登录
@app.route("/self_info", methods=['GET', 'POST'])
def check_self_info():
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    value1 = session['username']
    value5 = session['role']
    sql_1 = "SELECT phone_number FROM User WHERE user_name=%s"
    cursor.execute(sql_1, value1)
    phone = cursor.fetchone()["phone_number"]
    sql_2 = "SELECT role FROM User WHERE user_name=%s"
    cursor.execute(sql_2, value1)
    role = cursor.fetchone()
    if request.method == 'POST':
        value2 = request.form.get("old_password")
        value3 = request.form.get("new_password")
        value4 = request.form.get("confirm_password")
        sql1 = "SELECT * FROM User WHERE user_name =%s and password = %s"
        cursor.execute(sql1, (value1, value2))
        if cursor.fetchone() is None:
            m1 = "Tips: The password is wrong"
            return render_template('Account.html', message=m1, username=value1, role=value5,phone_number=phone)
        else:
            if value3 == value4:
                sql2 = "UPDATE User SET password= %s WHERE user_name = %s"
                cursor.execute(sql2, (value3, value1))
                conn.commit()
                return render_template('Account.html', message='Changed password successfully!', username=value1, role=value5,phone_number=phone)
            else:
                m2 = "Tips: The password entered twice is inconsistent"
                return render_template('Account.html', message=m2,  username=value1, role=value5,phone_number=phone)
    return render_template("Account.html",  username=value1, role=value5,phone_number=phone)

@app.route('/delete')
def delete():
    username=session['username']
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("DELETE FROM User WHERE user_name = %s", (username,))
    conn.commit()
    session.clear()
    return render_template('delete_success.html')







if __name__ == "__main__":
    app.run(port=5001, host="127.0.0.1", debug=True)

