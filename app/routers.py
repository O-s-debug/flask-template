import logging
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash
from utils import send_prediction_request
from forms import LoginForm, RegisterForm, PredictForm,ForgotPasswordForm, ResetPasswordForm

# Import from unified database.py
from database.database import decrypt, generate_recovery_code, get_user_by_phone, add_user, get_user_by_recovery_code, log_login_attempt, reset_password_db, send_recovery_email, set_recovery_code

router = Blueprint('router', __name__)

@router.route('/')
def landing_page():
    return render_template('index.html')

@router.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        phone = form.phone.data
        password = form.password.data
        ip = request.remote_addr

        user = get_user_by_phone(phone)
        if user and check_password_hash(user[5], password):  # password is at index 4
            session['name'] = user[1]
            session['phone'] = phone
            log_login_attempt(phone, success=True, ip_address=ip)
            return redirect(url_for('router.home'))
        else:
            log_login_attempt(phone, success=False, ip_address=ip)
            flash("Invalid phone number or password", "danger")
    return render_template('login.html', form=form)

@router.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        name = form.name.data
        phone = form.phone.data
        email = form.email.data
        password = form.password.data
        ip = request.remote_addr
        user_agent = request.headers.get('User-Agent')

        if add_user(name, phone, password, email, ip=ip, user_agent=user_agent):
            flash("Registration successful! Please login.", "success")
            return redirect(url_for('router.login'))
        else:
            flash("Phone number or email already registered!", "danger")
    return render_template('register.html', form=form)

@router.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('router.login'))

@router.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        phone = form.phone.data
        user = get_user_by_phone(phone)
        if user:
            code = generate_recovery_code()
            set_recovery_code(phone, code)
            try:
                email = decrypt(user[4])
            except Exception as e:
                logging.warning(f"Decryption failed: {e}")
                email = user[4]  # fallback to raw value (assume not encrypted)

            send_recovery_email(email, code)

            flash("Recovery code sent! Check your messages.", "success")
            return redirect(url_for('router.reset_password'))
        else:
            flash("Phone number not found.", "danger")
    return render_template("forgot_password.html", form=form)

@router.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        code = form.code.data
        new_password = form.new_password.data
        user = get_user_by_recovery_code(code)
        print(user)
        print(user[3])
        if user:
            reset_password_db(user[3], new_password)  # user[2] = phone
            flash("Password reset successful. Please log in.", "success")
            return redirect(url_for('router.login'))
        else:
            flash("Invalid recovery code.", "danger")
    return render_template("reset_password.html", form=form)


# main code

@router.route('/home')
def home():
    if 'name' in session:
        return render_template('home.html', username=session['name'], form=PredictForm())
    return redirect(url_for('router.login'))

@router.route('/predict', methods=['POST'])
def predict():
    if 'name' not in session:
        flash("Please login first.", "warning")
        return redirect(url_for('router.login'))

    form = PredictForm()
    if form.validate_on_submit():
        user_input = form.text.data
        result = send_prediction_request(user_input)
        return render_template('home.html', username=session['name'], result=result, form=PredictForm())

    flash("Invalid input", "warning")
    return redirect(url_for('router.home'))
