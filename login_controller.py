from sqlalchemy.exc import IntegrityError
from werkzeug.utils import redirect
import random
from config import *
from models import *
from flask import request, render_template
from werkzeug.security import generate_password_hash, check_password_hash

ALLOWED_IMAGE_FORMATS = ("jpg", "jpeg", "png", "gif")


@app.route('/', methods=['GET'])
def index_page():
    return render_template("index.html")


@app.route('/login', methods=['GET'])
def login_page():
    errors = {}
    msg = ""
    return render_template("login.html", message=msg, errors=errors, user="")


def validate_register_form(form_data, media_data):
    errors = {}
    if not form_data.get("fname") or len(form_data.get("fname")) <= 2:
        errors['err_name'] = "Invalid Name (Minimum 3 Characters Required)"
    if not form_data.get("lname") or len(form_data.get("lname")) <= 2:
        errors['err_name'] = "Invalid Name (Minimum 3 Characters Required)"
    if not form_data.get("email"):
        errors['err_email'] = "Invalid Email"
    elif form_data.get("email"):
        if UserInfo.query.filter_by(email=form_data.get("email")).first():
            errors['duplicate_email'] = f"Email {form_data.get('email')} Already Exists."

    if not form_data.get("contact"):
        errors['err_contact'] = "Invalid Contact"
    elif form_data.get("contact"):
        if UserInfo.query.filter_by(contact=form_data.get("contact")).first():
            errors['duplicate_contact'] = f"Contact {form_data.get('contact')} Already Exists."

    if not form_data.get("username") or len(form_data.get("username")) <= 2:
        errors['err_username'] = "Invalid Username (Minimum 3 Characters Required)"
    elif form_data.get("username"):
        if LoginInfo.query.filter_by(username=form_data.get("username")).first():
            errors['duplicate_username'] = f"Username {form_data.get('username')} Already Exists."

    if not form_data.get("password") or len(form_data.get("password")) <= 2:
        errors['err_password'] = "Invalid Password (Minimum 3 Characters Required)"
    if form_data.get("password") != form_data.get("password2"):
        errors['err_password2'] = "Passwords Do Not Match"
    if media_data:
        img_ext = media_data.filename.split(".")[-1]
        if img_ext.lower() in ALLOWED_IMAGE_FORMATS:
            print("Looking Wow !!\n")
            # print("ALLOWED FORMAT")
            # media_data.save("images/" + eid + "." + img_ext)
            # form_data.update({"photo": input_form.get('eid') + "." + img_ext})
        else:
            errors['err_password2'] = "Allowed Extensions: {}".format(ALLOWED_IMAGE_FORMATS)

    return errors


@app.route('/login', methods=['POST'])
def authenticate():
    errors = {}
    msg = ""
    if request.method == 'POST':
        form_data = request.form
        if form_data.get("username") and form_data.get("password"):
            user = form_data.get("username")
            pwd = form_data.get("password")
            # print("Username--->", user)
            # print("Password--->", pwd)
            login = LoginInfo.query.filter(LoginInfo.username == user).first()
            # print("LOGIN OBJ------>", login)
            # print("Check HASH--->", check_password_hash(login.password, pwd))
            if login and check_password_hash(login.password, pwd)\
                    and user.lower() == "admin" and login.user_status == 10:
                session['username'] = login.username
                return render_template("admin.html",
                                       message=msg,
                                       errors=errors,
                                       username=session['username'], )
            elif login and check_password_hash(login.password, pwd) and login.user_status == 10:
                session['username'] = login.username
                image_name = login.userref.image
                print("------------------>", image_name)
                return render_template("home.html",
                                       message=msg,
                                       errors=errors,
                                       username=session.get('username'),
                                       image_name=image_name)
            elif login and check_password_hash(login.password, pwd) and login.user_status == 11:
                user_email = login.userref.email
                pending = "Your Verification is Pending..! Please Verify Email"
                return render_template("send_otp.html",
                                       pending=pending,
                                       message=msg,
                                       errors=errors,
                                       form_data=form_data,
                                       username='',
                                       user_mail=user_email)
            else:
                msg = "Invalid Credentials"
                return render_template("login.html", message=msg, errors=errors, user="")
        else:
            msg = "Please Enter Username and Password"
            return render_template("login.html", message=msg, errors=errors, user="")
    else:
        return redirect(location='/')
        # return redirect(url_for('/'))
        # return render_template("login.html", message=msg, errors=errors)


@app.route('/register', methods=['POST', 'GET'])
def register_user():
    msg = ""
    resume_data = {
        "fname": "",
        "lname": "",
        "city": "",
        "email": "",
        "contact": "",
        "username": "",
        "password": "",
        "password2": "",
    }
    courses = Course.query.all()
    if request.method == 'POST':
        form_data = request.form
        media_data = request.files['image']
        errors = validate_register_form(form_data, media_data)
        if not errors:
            user = LoginInfo.query.filter(LoginInfo.username == form_data['username']).first()
            if user:
                msg = f'Username {form_data.get("username")} Not Available !!'
                return render_template("register.html",
                                       message=msg,
                                       errors={},
                                       form_data=form_data,
                                       courses=courses)
            else:
                try:
                    new_user = UserInfo(fname=form_data.get("fname"),
                                        lname=form_data.get("lname"),
                                        email=form_data.get("email"),
                                        contact=form_data.get("contact"),
                                        city=form_data.get("city"),
                                        gender=form_data.get("gender"),
                                        image="", )
                    print(new_user.__dict__)

                    db.session.add(new_user)
                    db.session.commit()

                    # Code for saving Image
                    eid = new_user.id
                    img_ext = media_data.filename.split(".")[-1]
                    image_name = str(eid) + "." + img_ext
                    media_data.save("static/" + image_name)
                    new_user.image = image_name
                    db.session.commit()

                    new_login = LoginInfo(username=form_data.get("username"),
                                          password=generate_password_hash(form_data.get("password")))
                    new_login.user_id = new_user.id

                    print(new_login.__dict__)
                    db.session.add(new_login)
                    db.session.commit()
                    print("Courses Interested --->", form_data.getlist("courses"))

                    for cid in form_data.getlist("courses"):
                        course = Course.query.filter_by(id=cid).first()
                        new_user.courses_list.append(course)

                    # active_status = UserStatus.query.filter_by(status="Active").first()
                    # pending_status = UserStatus.query.filter_by(status="Verification Pending").first()
                    new_login.user_status = 11  # 11 is for "Verification Pending"

                    # current_role = Role.query.filter_by(role="Student").first()
                    # new_login.roleref = current_role
                    new_login.user_role = 502   # 502 is for "Student"

                    db.session.commit()
                    # return render_template("login.html", message=msg, errors={}, form_data=form_data)
                except IntegrityError as e:
                    # print(type(e))
                    print("-------------->", e)
                    print("~~~~~~~~~~~~~~~")
                    s = e.args[0].split(", ")[-1][1:-2]
                    val = s.split("'")[1]
                    col = s.split("'")[-2].split(".")[-1].title()
                    msg = f"Duplicate Entry {val} for {col}"
                    print(msg)
                    return render_template("register.html",
                                           message=msg,
                                           errors={},
                                           form_data=form_data, user="",
                                           courses=courses)
                else:
                    msg = f"User {new_login.username} Created"

                    # Sending OTP as soon as we register
                    # otp = random.randint(100000, 999999)
                    # email_msg = Message('Verify Email', sender='fashionadda.ab@gmail.com',
                    #                     recipients=[new_user.email])
                    # email_msg.body = f"Your Verification Code is {otp}"
                    # mail.send(email_msg)

                    return render_template("send_otp.html",
                                           message=msg,
                                           errors=errors,
                                           form_data=form_data,
                                           username=new_login.username,
                                           user_mail=new_user.email)
                    # return render_template("login.html",
                    #                        message=msg,
                    #                        errors=errors,
                    #                        form_data=form_data,
                    #                        username=new_login.username)
        else:
            return render_template("register.html",
                                   message=msg,
                                   errors=errors,
                                   form_data=form_data,
                                   courses=courses)
    return render_template("register.html",
                           message=msg,
                           errors={},
                           form_data=resume_data,
                           courses=courses)


@app.route("/logout", methods=['GET'])
def logout():
    if session.get("username"):
        session.pop("username")
    errors = {}
    msg = ""
    return render_template("login.html", message=msg, errors=errors, username="")


@app.route("/", methods=['GET', 'POST'])
def register_page():
    pass
