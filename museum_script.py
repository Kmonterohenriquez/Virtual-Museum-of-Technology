import datetime
from functools import wraps
from flask import Flask, render_template, request, redirect, flash, url_for, session
from wtforms import Form, StringField, PasswordField, SubmitField, validators, ValidationError
import mysql.connector
from passlib.hash import sha256_crypt

app = Flask(__name__)
app.secret_key = 'SHH!'

# Configuring db
db = mysql.connector.connect(host='localhost', port=3306, database='virtual_museum', user='root', password='museum',
                             auth_plugin='mysql_native_password')

# ---------------CLASS - REGISTRATION FORM ----------#

class SignUpForm(Form):
    # --------------->   Payment info    <-----------------------------------
    card_number = StringField('', [validators.length(min=16, max=19),
                                   validators.Regexp('\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}',
                                                     message='Please insert a valid card number!')])
    exp_date = StringField('', [validators.length(5),
                                validators.Regexp('\d{2}[/-]\d{2}',
                                                  message='Expiration date is not valid!')])
    cvv = StringField('', [validators.length(3),
                           validators.Regexp('\d{3}',
                                             message='Card code inserted is not valid!')])

    # --------------->   User info    <-----------------------------------
    firstName = StringField('', [validators.length(min=1, max=50),
                                 validators.Regexp('([A-Z][a-z]*)([\\s\\\'-][A-Z][a-z]*)*',
                                                   message='Please enter a valid name!')])
    lastName = StringField('', [validators.length(min=1, max=50),
                                validators.Regexp('([A-Z][a-z]*)([\\s\\\'-][A-Z][a-z]*)*',
                                                  message='Please enter a valid name!')])
    email = StringField('', [validators.length(min=4, max=100),
                             validators.Regexp('[^@]+@[^@]+\.[^@]+', message='Please enter a valid email!')])
    password = PasswordField('', [validators.DataRequired(),
                                  validators.EqualTo('pwConfirm', message='Passwords must match!')])
    pwConfirm = PasswordField('')

    submit = SubmitField('Submit')

# --------------->>  STORE   <<------------------------------------
class storeForm(Form):
    submit = SubmitField('Submit')

class cartForm(Form):
    submit = SubmitField('Submit')



#---------------->>  CHECK OUT  <<---------------------------------
class CheckOut(Form):
    card_number = StringField('', [validators.length(min=16, max=19),
                                   validators.Regexp('\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}',
                                                     message='Please insert a valid card number!')])
    exp_date = StringField('', [validators.length(5),
                                validators.Regexp('\d{2}[/-]\d{2}',
                                                  message='Please insert a valid Expiration Date')])
    cvv = StringField('', [validators.length(3),
                           validators.Regexp('\d{3}',
                                             message='Card code inserted is not valid!')])
    submit = SubmitField('submit')


# --------------->  Class Security    <-----------------------------------
class SecureForm(Form):
    answer_one = StringField('', [validators.length(min=3, max=16), validators.data_required()])
    answer_two = StringField('', [validators.length(min=3, max=16), validators.data_required()])
    answer_three = StringField('', [validators.length(min=3, max=16), validators.data_required()])
    submit = SubmitField('Submit')

# --------- FUNCTIONS ------------#

# - FUNCTION THAT CHECKS IF USER IS LOGGED IN
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("You must be logged in to access this room!", 'danger')
            return redirect('/login')
    return wrap


# LOGOUT ROUTE
@app.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('home'))


# ------------------ LOGGED OUT PAGES ----------------#
# -- HOME LANDING PAGE - MUSEUM FRONT

@app.route('/', methods=['POST', 'GET'])
def home():
    try:
        email = session['email']
        return redirect('/main')
    except:
        return render_template("home.html")

# ----------------------------USER REGISTRATION ---------------------------------#
@app.route('/signup', methods=['POST', 'GET'])
def signup():
    form = SignUpForm(request.form)

    # if the user is inputing information it will be assigned to the below variables and sent to the database
    if request.method == 'POST' and form.validate():
        try:
            # USER INFORMATION
            firstName = form.firstName.data
            lastName = form.lastName.data
            email = form.email.data
            password = sha256_crypt.encrypt(str(form.password.data))
            date_created = datetime.datetime.today().strftime('%Y-%m-%d')


            # CARD INFORMATION
            card_number = form.card_number.data
            exp_date = form.exp_date.data
            cvv = form.cvv.data

            question_one = '48$%*($*#&'
            question_two = '48$%*($*#&'
            question_three = '48$%*($*#&'
            answer_one = '48$%*($*#&'
            answer_two = '48$%*($*#&'
            answer_three = '48$%*($*#&'
            cursor = db.cursor()
            cursor.execute(
                'INSERT INTO user_info(first_name,last_name,email,password,date_created,question_one,question_two,'
                'question_three,answer_one,answer_two,answer_three,card_number, exp_date, cvv) '
                'VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                (firstName, lastName, email, password, date_created, question_one, question_two, question_three,
                 answer_one, answer_two, answer_three, card_number, exp_date, cvv))
            db.commit()
            cursor.close()
            return redirect("/store")

        except Exception as e:
            app.logger.info(e)
            flash('There is a member registered with this email already, please re-enter the information!', 'danger')

    return render_template("sign_up.html", form=form, debug=True)


# --------------------------------USER LOG IN-----------------------------#
@app.route('/login', methods=['POST', 'GET'])
def logIn():
    global check_email

    # statements to check if users inputs the correct information such as username(email) and password
    if request.method == 'POST':
        email = request.form['email']
        password_try = request.form['password']
        cursor = db.cursor(dictionary=True, buffered=True)
        result = cursor.execute("SELECT * FROM user_info WHERE email = %s", [email])

        if result is not 0:  # checking information input by user
            data = cursor.fetchone()

            try:
                password = data['password']

                if sha256_crypt.verify(password_try, password):

                    app.logger.info('PASSWORD MATCHED')
                    cursor.execute("SELECT first_name FROM user_info WHERE email = %s", [email])
                    name_retrieve = cursor.fetchone()
                    name = name_retrieve['first_name']
                    session['logged_in'] = True
                    session['name'] = name

                    cursor.execute("SELECT email FROM user_info WHERE email = %s", [email])
                    email_retrieve = cursor.fetchone()
                    em = email_retrieve['email']
                    session['email'] = em

                    cursor.execute("SELECT date_created FROM user_info WHERE email = %s", [email])
                    date_retrieve = cursor.fetchone()
                    date = date_retrieve['date_created'].strftime('%m-%d-%Y')
                    session['date'] = date

                    cursor.execute("SELECT answer_one FROM user_info WHERE email = %s", [email])
                    answer_retrieve = list(cursor.fetchone().values())
                    answer = answer_retrieve[0]
                    app.logger.info(answer)

                    # CHECKING IF ANSWERS HAVE BEEN SET
                    if answer == '48$%*($*#&':

                        check_email = email
                        app.logger.info(check_email)
                        cursor.close()
                        return redirect('/security_setup')
                    else:
                        cursor.close()
                        return redirect('/main')
                    cursor.close()

                else:
                    app.logger.info('PASSWORD NOT MATCHED')
                    flash('The email or password entered is not valid! Please try Again!', 'danger')
            except:
                app.logger.info('NO USER')
                flash('The email or password entered is not valid! Please try Again!', 'danger')
        else:
            app.logger.info('NO USER')

        # closing connection
        cursor.close()

    return render_template("login.html")

# -------------------------------------------------------SECURITY QUESTIONS SETUP AND CHECK -----------------------#

@app.route('/security_setup', methods=['POST', 'GET'])
def security_setup():
    form = SecureForm(request.form)

    petName = 'What is the name of your first pet?'
    bestFriend = 'Who is your best friend?'
    favBook = 'What is your favorite book?'
    favVideoGame = 'What is your favorite video game?'
    favSport = 'What is your favorite sport?'
    choice = [petName, bestFriend, favBook, favVideoGame, favSport]

    if request.method == 'POST' and form.validate():
        try:
            question_one = str(request.form.get('selection'))
            question_two = str(request.form.get('selection_two'))
            question_three = str(request.form.get('selection_three'))
            app.logger.info(question_one)
            answer_one = str(request.form['answer_one'])
            answer_two = str(request.form['answer_two'])
            answer_three = str(request.form['answer_three'])
            app.logger.info(answer_one)
            cursor = db.cursor()

            try:
                if session['name'] is not 0:
                    cursor.execute('SELECT account_number FROM user_info WHERE email = %s', [check_email])
                    selection = cursor.fetchone()
                    acct = str(selection[0])
                    app.logger.info(acct)
                    cursor.execute(
                        'UPDATE user_info SET question_one = %s, answer_one = %s, question_two = %s, answer_two = %s, question_three = %s, answer_three = %s WHERE account_number = %s',
                        (question_one, answer_one, question_two, answer_two, question_three, answer_three, acct))
                    flash('Thank you for setting up the security questions! Enjoy the museum!', 'success')
                    db.commit()
                    cursor.close()
                    return redirect("/museum")

                else:
                    cursor.execute('SELECT account_number FROM user_info ORDER BY account_number DESC LIMIT 1')
                    selection = cursor.fetchone()
                    acct = str(selection[0])
                    app.logger.info(acct)
                    cursor.execute(
                    'UPDATE user_info SET question_one = %s, answer_one = %s, question_two = %s, answer_two = %s, question_three = %s, answer_three = %s WHERE account_number = %s',
                    (question_one, answer_one, question_two, answer_two, question_three, answer_three, acct))
                    db.commit()
                    cursor.close()

                flash('You are now registered and can log in!', 'success')
                return redirect("/login")

            except:
                cursor.execute('SELECT account_number FROM user_info ORDER BY account_number DESC LIMIT 1')
                selection = cursor.fetchone()
                acct = str(selection[0])
                app.logger.info(acct)
                cursor.execute(
                'UPDATE user_info SET question_one = %s, answer_one = %s, question_two = %s, answer_two = %s, question_three = %s, answer_three = %s WHERE account_number = %s',
                (question_one, answer_one, question_two, answer_two, question_three, answer_three, acct))
                db.commit()
                cursor.close()

                flash('You are now registered and can log in!', 'success')
                return redirect("/login")

        except Exception as e:
            app.logger.info(e)
            flash('Something is wrong', 'danger')
    else:
        app.logger.info('NO !')

    items_1_on_cart, items_2_on_cart, items_3_on_cart, items_4_on_cart, items_on_cart, empty_cart = display_items()

    return render_template("security.html", form=form, choice=choice, debug=True, items_1_on_cart=items_1_on_cart, items_2_on_cart=items_2_on_cart,
                           items_3_on_cart=items_3_on_cart, items_4_on_cart=items_4_on_cart,items_on_cart=items_on_cart)


# --FORGOT LOGIN---------------#
@app.route('/forgotten_login', methods=['POST', 'GET'])
def forgot_login():
    global email_reset

    if request.method == 'POST':
        email = request.form['email']
        email_reset = email

        return redirect('/security_check')
    return render_template("forgot_login.html", debug=True)


# --- Security Check------------#
@app.route('/security_check', methods=['POST', 'GET'])
def security_check():
    form = SecureForm(request.form)

    cursor = db.cursor(dictionary=True, buffered=True)

    try:
        cursor.execute('SELECT question_one FROM user_info WHERE email = %s', [email_reset])
        question_one_retrieve = list(cursor.fetchone().values())
        first_question = question_one_retrieve[0]
        session['question_one'] = first_question

        cursor.execute('SELECT question_two FROM user_info WHERE email = %s', [email_reset])
        question_two_retrieve = list(cursor.fetchone().values())
        second_question = question_two_retrieve[0]
        session['question_two'] = second_question

        cursor.execute('SELECT question_three FROM user_info WHERE email = %s', [email_reset])
        question_three_retrieve = list(cursor.fetchone().values())
        third_question = question_three_retrieve[0]
        session['question_three'] = third_question

        if request.method == 'POST':
            input_answer_one = request.form['answer_one']
            input_answer_two = request.form['answer_two']
            input_answer_three = request.form['answer_three']
            result = cursor.execute('SELECT * FROM user_info WHERE email = %s', [email_reset])

            if result is not 0:
                retrieve = cursor.fetchone()

                try:
                    ans_one = retrieve['answer_one']
                    ans_two = retrieve['answer_two']
                    ans_three = retrieve['answer_three']

                    if ans_one == input_answer_one and ans_two == input_answer_two and ans_three == input_answer_three:
                        app.logger.info('They matched!')
                        flash('You may now reset your password!','success')
                        return redirect('/reset_login')
                    else:
                        app.logger.info('They did not match!')
                        flash('One of your answers is not correct. Please try again!','danger')
                except Exception as e:
                    app.logger.info(e)

    except Exception as f:
        app.logger.info(f)
        flash('Please re-enter the email!', 'danger')
        return redirect('/forgotten_login')

    return render_template("forgot_login2.html", form=form, debug=True)


# --RESET LOGIN
@app.route('/reset_login',methods=['POST', 'GET'])
def reset_login():
    form = SignUpForm(request.form)

    if request.method == 'POST':
        password = sha256_crypt.encrypt(str(form.password.data))
        cursor = db.cursor()
        cursor.execute('UPDATE user_info SET password = %s WHERE email = %s',(password , email_reset))
        db.commit()
        cursor.close()
        flash('The password has been reset successfully! Please login!', 'success')
        return redirect('/login')

    return render_template("reset_login.html", form = form, debug = True)

# ---------------->   DISPLAYING ITEMS ON THE CART  <-------------------#
def display_items():
    email = session['email']
    cursor = db.cursor()
    # ---------------->   ING ITEMS ON THE CART  <-------------------#
    cursor.execute("SELECT account_number FROM user_info WHERE email = %s", [email])
    acct = cursor.fetchone()[0]

    # -How many Items 1  on the cart
    cursor.execute('SELECT COUNT(item_id) FROM cart WHERE account_number = %s AND item_id= %s', (acct, 1))
    items_1_on_cart = cursor.fetchone()[0]

    # -How many Items 2  on the cart
    cursor.execute('SELECT COUNT(item_id) FROM cart WHERE account_number = %s AND item_id= %s', (acct, 2))
    items_2_on_cart = cursor.fetchone()[0]

    # -How many Items 3 on the cart
    cursor.execute('SELECT COUNT(item_id) FROM cart WHERE account_number = %s AND item_id= %s', (acct, 3))
    items_3_on_cart = cursor.fetchone()[0]

    # -How many Itemss 4 on the cart
    cursor.execute('SELECT COUNT(item_id) FROM cart WHERE account_number = %s AND item_id= %s', (acct, 4))
    items_4_on_cart = cursor.fetchone()[0]

    # -How many Items are/is on the cart
    cursor.execute('SELECT COUNT(item_id) FROM cart WHERE account_number = %s', [acct])
    items_on_cart = cursor.fetchone()[0]

    # ---------------->   EMPTY CART  <-------------------#
    empty_cart = 0
    if empty_cart == items_on_cart:
        empty_cart = 'cart is empty'

    return (items_1_on_cart, items_2_on_cart, items_3_on_cart, items_4_on_cart, items_on_cart, empty_cart)

# ------------------ LOGGED IN PAGES ----------------#
@app.route('/main')
@is_logged_in
def mainRoom():
    items_1_on_cart, items_2_on_cart, items_3_on_cart, items_4_on_cart, items_on_cart, empty_cart = display_items()

    return render_template("home.html",items_1_on_cart=items_1_on_cart , items_2_on_cart=items_2_on_cart,
                           items_3_on_cart=items_3_on_cart, items_4_on_cart=items_4_on_cart, items_on_cart=items_on_cart)


#-------------------------->   Working on this area   <---------------------------------#

# @app.route('/games',methods=['POST', 'GET'])
# @is_logged_in
# def games():
#     email = session['email']
#     cursor = db.cursor()
#     cursor.execute("SELECT score FROM user_info WHERE email = %s", [email])
#     score = cursor.fetchone()[0]
#     app.logger.info(score)
#
#     user_score_html = request.args.get('score')
#     app.logger.info(user_score_html)
#
#     if user_score_html is not None:
#         cursor.execute('UPDATE user_info SET score = %s WHERE email = %s',(user_score_html,email))
#         db.commit()
#         cursor.close()
#     # ---------------->   DISPLAY ITEMS ON THE CART  <-------------------#
#     items_1_on_cart, items_2_on_cart, items_3_on_cart, items_4_on_cart, items_on_cart, empty_cart = display_items()
#
#     return render_template("games.html", debug=True, items_1_on_cart=items_1_on_cart,items_2_on_cart=items_2_on_cart,
#                             items_3_on_cart=items_3_on_cart, items_4_on_cart=items_4_on_cart,
#                             items_on_cart=items_on_cart, empty_cart=empty_cart)


# --STORE
@app.route('/store',methods=['POST', 'GET'])
@app.route('/_cart_modal', methods=['POST', 'GET'])
@is_logged_in
def store():
    form = storeForm(request.form)
    email = session['email']
    cursor = db.cursor()
    cursor.execute("SELECT account_number FROM user_info WHERE email = %s", [email])
    acct = cursor.fetchone()[0]

    #----------------> Adding item on the cart <---------------------#
    if request.method == 'POST':
        if request.form['itemOne'] == 'itemOne':
            cursor.execute('INSERT INTO cart(account_number,item_id) VALUES(%s,%s)', (acct, 1))

        elif request.form['itemOne'] == 'itemTwo':
            cursor.execute('INSERT INTO cart(account_number,item_id) VALUES(%s,%s)',(acct, 2))

        elif request.form['itemOne'] == 'itemThree':
            cursor.execute('INSERT INTO cart(account_number,item_id) VALUES(%s,%s)',(acct,3))

        elif request.form['itemOne'] == 'itemFour':
            cursor.execute('INSERT INTO cart(account_number,item_id) VALUES(%s,%s)',(acct, 4))
        return redirect('/store')


        # Submiting data into DataBase
        db.commit()
        # Closing cursor
        cursor.close()

    # ---------------->   DISPLAY ITEMS ON THE CART  <-------------------#
    items_1_on_cart, items_2_on_cart, items_3_on_cart, items_4_on_cart, items_on_cart, empty_cart = display_items()


    return render_template("store.html", debug= True, items_1_on_cart=items_1_on_cart , items_2_on_cart=items_2_on_cart,
                           items_3_on_cart=items_3_on_cart, items_4_on_cart=items_4_on_cart, items_on_cart=items_on_cart, empty_cart=empty_cart)

#-- CHECK OUT
@app.route('/check_out',methods=['POST', 'GET'])
@is_logged_in
def check_out():
    form = CheckOut(request.form)
    email = session['email']
    cursor = db.cursor()

    #- CURRENT ACCOUNT
    cursor.execute("SELECT account_number FROM user_info WHERE email = %s", [email])
    acct = cursor.fetchone()[0]

    # ---------------->   DISPLAY ITEMS ON THE CART  <-------------------#
    items_1_on_cart, items_2_on_cart, items_3_on_cart, items_4_on_cart, items_on_cart, empty_cart = display_items()

    # -ITEM'S PRICES
    item_1_price = 4.50
    item_2_price = 5.50
    item_3_price = 6.50
    item_4_price = 7.50

    # -TOTAL FOR EACH ITEM
    item_1_total = items_1_on_cart * item_1_price
    item_2_total = items_2_on_cart * item_2_price
    item_3_total = items_3_on_cart * item_3_price
    item_4_total = items_4_on_cart * item_4_price

    # -TOTAL PRICE
    items_total_price = item_1_total + item_2_total + item_3_total + item_4_total
    # ----------------> Deleting item from the cart <---------------------#
    # cursor.execute(
    #     'SELECT *, ROW_NUMBER()OVER(PARTITION BY item_id ORDER BY item_id) AS RowNumber FROM cart WHERE account_number = %s;',
    #     [acct])
    # db.commit()
    # cursor.execute('DELETE FROM cart WHERE RowNumber = 1 AND item_id = 1')

    # if request.method == 'POST':
    #     if request.form['item-1'] == 'delete-1':
    #         cursor.execute('DELETE FROM cart WHERE account_number = %s and item_id =%s', (acct, 1))
    #
    #     elif request.form['item-2'] == 'delete-2':
    #         cursor.execute('DELETE FROM cart WHERE account_number = %s and item_id =%s', (acct, 2))
    #
    #     elif request.form['item-3'] == 'delete-3':
    #         cursor.execute('DELETE FROM cart WHERE account_number = %s and item_id =%s', (acct, 3))
    #
    #     elif request.form['item-4'] == 'delete-4':
    #         cursor.execute('DELETE FROM cart WHERE account_number = %s and item_id =%s', (acct, 4))
    #     return redirect('/check_out')
    #     db.commit()

    #------------------------------->> PAYMENT AREA <<-------------------------------------------#
    if request.method == 'POST' and form.validate():

        #- COMPARING INSERTED INFO WITH THE DB
        if request.form['check_out'] == 'check_out':
            #  PAYMENT INFO
            card_number = str(request.form['card_number'])
            exp_date = str(request.form['exp_date'])
            cvv = str(request.form['cvv'])

            # GETTING PAYMENT INFO FROM DB
            cursor.execute('SELECT card_number FROM user_info WHERE account_number = %s', [acct])
            card_number_registered = cursor.fetchone()[0]
            cursor.execute('SELECT exp_date FROM user_info WHERE account_number = %s', [acct])
            exp_date_registered = cursor.fetchone()[0]
            cursor.execute('SELECT cvv FROM user_info WHERE account_number = %s', [acct])
            cvv_registered = cursor.fetchone()[0]

            # CHECKING IF THE INFO PROVIDED BY THE USER IS THE SAME REGISTERED ON DB
            if (card_number == card_number_registered) and (exp_date == exp_date_registered) and (cvv == cvv_registered):
                cursor.execute('DELETE FROM cart WHERE account_number = %s', [acct])
                flash('Thank you for shopping in Virtual Museum of Technology.','success')
                db.commit()
                return  redirect('/check_out')
            else:
                flash('This card information is not registered, please try again.', 'danger')


    # -Submiting data to the database
    db.commit()
    # Closing Cursor
    cursor.close()

    return render_template("check_out.html",items_1_on_cart=items_1_on_cart , items_2_on_cart=items_2_on_cart,
                           items_3_on_cart=items_3_on_cart, items_4_on_cart=items_4_on_cart, items_total_price=items_total_price,items_on_cart=items_on_cart, empty_cart=empty_cart, form=form)

# --MUSEUM
@app.route('/museum')
@is_logged_in
def museum():
    return render_template("museum_p1.html")


# --PROFILE
@app.route('/profile',methods=['POST', 'GET'])
@is_logged_in
def profile():

    email = session['email']
    app.logger.info(email)
    cursor = db.cursor()
    cursor.execute("SELECT answer_one FROM user_info WHERE email = %s", [email])
    result = cursor.fetchone()[0]
    app.logger.info(result)

    cursor.execute("SELECT player_score FROM user_info WHERE email = %s", [email])
    score_retrieve = cursor.fetchone()[0]
    session['score'] = score_retrieve
    app.logger.info(score_retrieve)


    if result == '48$%*($*#&':
        answer_check = False
    else:
        answer_check = True

    app.logger.info(answer_check)


    # ---------------->   DISPLAY ITEMS ON THE CART  <-------------------#
    items_1_on_cart, items_2_on_cart, items_3_on_cart, items_4_on_cart, items_on_cart, empty_cart = display_items()

    return render_template("profile.html",answer_check=answer_check, items_1_on_cart=items_1_on_cart , items_2_on_cart=items_2_on_cart,
                           items_3_on_cart=items_3_on_cart, items_4_on_cart=items_4_on_cart, items_on_cart=items_on_cart, empty_cart=empty_cart)


@app.route('/about')
@is_logged_in
def about():
    # ---------------->   DISPLAY ITEMS ON THE CART  <-------------------#
    items_1_on_cart, items_2_on_cart, items_3_on_cart, items_4_on_cart, items_on_cart, empty_cart = display_items()

    return render_template("about.html", items_1_on_cart=items_1_on_cart , items_2_on_cart=items_2_on_cart,
                           items_3_on_cart=items_3_on_cart, items_4_on_cart=items_4_on_cart, items_on_cart=items_on_cart, empty_cart=empty_cart)

@app.route('/1960')
@is_logged_in
def test():
    # ---------------->   DISPLAY ITEMS ON THE CART  <-------------------#
    items_1_on_cart, items_2_on_cart, items_3_on_cart, items_4_on_cart, items_on_cart, empty_cart = display_items()

    return render_template("1960.html",items_1_on_cart=items_1_on_cart , items_2_on_cart=items_2_on_cart,
                           items_3_on_cart=items_3_on_cart, items_4_on_cart=items_4_on_cart, items_on_cart=items_on_cart, empty_cart=empty_cart)


@app.route('/1970')
@is_logged_in
def _1970():
    # ---------------->   DISPLAY ITEMS ON THE CART  <-------------------#
    items_1_on_cart, items_2_on_cart, items_3_on_cart, items_4_on_cart, items_on_cart, empty_cart = display_items()

    return render_template("1970.html",items_1_on_cart=items_1_on_cart , items_2_on_cart=items_2_on_cart,
                           items_3_on_cart=items_3_on_cart, items_4_on_cart=items_4_on_cart, items_on_cart=items_on_cart, empty_cart=empty_cart)


@app.route('/1980')
@is_logged_in
def _1980():
    # ---------------->   DISPLAY ITEMS ON THE CART  <-------------------#
    items_1_on_cart, items_2_on_cart, items_3_on_cart, items_4_on_cart, items_on_cart, empty_cart = display_items()

    return render_template("1980.html",items_1_on_cart=items_1_on_cart , items_2_on_cart=items_2_on_cart,
                           items_3_on_cart=items_3_on_cart, items_4_on_cart=items_4_on_cart, items_on_cart=items_on_cart, empty_cart=empty_cart)


@app.route('/1990')
@is_logged_in
def _1990():
    # ---------------->   DISPLAY ITEMS ON THE CART  <-------------------#
    items_1_on_cart, items_2_on_cart, items_3_on_cart, items_4_on_cart, items_on_cart, empty_cart = display_items()

    return render_template("1990.html",items_1_on_cart=items_1_on_cart , items_2_on_cart=items_2_on_cart,
                           items_3_on_cart=items_3_on_cart, items_4_on_cart=items_4_on_cart, items_on_cart=items_on_cart, empty_cart=empty_cart)


@app.route('/2000')
@is_logged_in
def _2000():
    # ---------------->   DISPLAY ITEMS ON THE CART  <-------------------#
    items_1_on_cart, items_2_on_cart, items_3_on_cart, items_4_on_cart, items_on_cart, empty_cart = display_items()

    return render_template("2000.html", items_1_on_cart=items_1_on_cart , items_2_on_cart=items_2_on_cart,
                           items_3_on_cart=items_3_on_cart, items_4_on_cart=items_4_on_cart, items_on_cart=items_on_cart, empty_cart=empty_cart)


@app.route('/2010')
@is_logged_in
def _2010():
    # ---------------->   DISPLAY ITEMS ON THE CART  <-------------------#
    items_1_on_cart, items_2_on_cart, items_3_on_cart, items_4_on_cart, items_on_cart, empty_cart = display_items()

    return render_template("2010.html", items_1_on_cart=items_1_on_cart , items_2_on_cart=items_2_on_cart,
                           items_3_on_cart=items_3_on_cart, items_4_on_cart=items_4_on_cart, items_on_cart=items_on_cart, empty_cart=empty_cart)


if __name__ == '__main__':
    app.run(debug=True)
