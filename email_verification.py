from config import *
import random
from models import *

system_otp = random.randint(100000, 999999)
mail = Mail(app)


@app.route("/send_otp", methods=['GET', 'POST'])
def send_otp():
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
    if request.method == 'POST':
        user_email = request.form.get("email")
        user = UserInfo.query.filter_by(email=user_email).first()
        if user:
            msg = Message('Verify Account', sender='fashionadda.ab@gmail.com', recipients=[user_email])
            msg.body = f"Your Verification Code is {system_otp}"
            mail.send(msg)
            session['user_email'] = user_email
            return render_template("verify_otp.html", user_email=user_email)
        else:
            need_to_register = f"No account is registered with {user_email}. Kindly Register First."
            return render_template("register.html",
                                   need_to_register=need_to_register,
                                   form_data=resume_data,
                                   errors={})
    return render_template("send_otp.html")


@app.route("/verify_otp", methods=['GET', 'POST'])
def verify_otp():
    failure = None
    counter = 4
    if request.method == 'POST':
        user_otp = request.form.get("otp")
        if int(user_otp) == system_otp and counter > 0:
            success = "You have successfully Verified your Account. You can login now."
            user_email = session.get("user_email")
            session.pop('user_email')
            user = UserInfo.query.filter_by(email=user_email).first()
            user.loginref.user_status = 10  # 10 is for active
            db.session.commit()
            return render_template("login.html", success=success)
        else:
            counter -= 1
            failure = f"You entered wrong otp. Please try again ({counter} Chances Left)."

        return render_template("verify_otp.html", failure=failure)
    return render_template("verify_otp.html")
