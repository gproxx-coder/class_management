from config import *
from models import *


@app.route('/home', methods=['GET'])
def home_page():
    msg = ""
    if session.get("username"):
        errors = {}
        msg = ""
        username = session.get("username")
        image_name = LoginInfo.query.filter_by(username=username).first().userref.image
        return render_template("home.html", message=msg,
                               errors=errors,
                               username=username,
                               image_name=image_name)

    return render_template("login.html",
                           message=msg,
                           user="")


@app.route('/home/course', methods=['GET'])
def home_course():
    msg = ""
    if session.get("username"):
        errors = {}
        username = session.get("username")
        all_courses = Course.query.all()
        image_name = LoginInfo.query.filter_by(username=username).first().userref.image
        return render_template("user_course_view.html",
                               message=msg,
                               errors=errors,
                               username=username,
                               all_courses=all_courses,
                               image_name=image_name)

    return render_template("login.html",
                           message=msg,
                           user="")


@app.route('/home/batch', methods=['GET'])
def home_batch():
    msg = ""
    if session.get("username"):
        errors = {}
        username = session.get("username")
        all_batches = Batch.query.all()
        image_name = LoginInfo.query.filter_by(username=username).first().userref.image
        return render_template("user_batch_view.html",
                               message=msg,
                               errors=errors,
                               username=username,
                               all_batches=all_batches,
                               image_name=image_name)

    return render_template("login.html",
                           message=msg,
                           user="")


@app.route('/home/user', methods=['GET'])
def home_users():
    msg = ""
    if session.get("username"):
        errors = {}
        final_batch_mates = []
        username = session.get("username")
        user_batches_list = LoginInfo.query.filter_by(username=username).first().userref.batches_list

        for batch in user_batches_list:
            users = batch.users_list
            for user in users:
                final_batch_mates.append(user)

        final_batch_mates = list(set(final_batch_mates))

        image_name = LoginInfo.query.filter_by(username=username).first().userref.image
        return render_template("user_batch_mates_view.html",
                               message=msg,
                               errors=errors,
                               username=username,
                               final_batch_mates=final_batch_mates,
                               image_name=image_name)

    return render_template("login.html",
                           message=msg,
                           user="")


@app.route('/home/profile', methods=['GET'])
def home_profile():
    msg = ""
    if session.get("username"):
        errors = {}
        final_batch_mates = []
        username = session.get("username")
        if request.method == "POST":
            pass

        image_name = LoginInfo.query.filter_by(username=username).first().userref.image
        login = LoginInfo.query.filter_by(username=username).first()
        return render_template("my_profile.html",
                               message=msg,
                               errors=errors,
                               username=username,
                               image_name=image_name,
                               login=login,
                               )

    return render_template("login.html",
                           message=msg,
                           user="")


@app.route('/home/profile/edit', methods=['GET'])
def home_profile_edit():
    msg = ""
    if session.get("username"):
        errors = {}
        username = session.get("username")

        image_name = LoginInfo.query.filter_by(username=username).first().userref.image
        login = LoginInfo.query.filter_by(username=username).first()
        return render_template("my_profile_edit.html",
                               message=msg,
                               errors=errors,
                               username=username,
                               image_name=image_name,
                               login=login,
                               )

    return render_template("login.html",
                           message=msg,
                           user="")


@app.route('/home/profile/update', methods=['POST', 'GET'])
def home_profile_update():
    msg = ""
    if session.get("username"):
        errors = {}
        username = session.get("username")
        if request.method == "POST":
            # Updating the user profile [fname, lname, email, contact, city, Image(if chosen)]
            media_data = request.files['image']
            user = LoginInfo.query.filter_by(username=username).first().userref

            if media_data:
                eid = user.id
                img_ext = media_data.filename.split(".")[-1]
                image_name = str(eid) + "." + img_ext

                media_data.save("static/" + image_name)

            user.fname = request.form.get('fname')
            user.lname = request.form.get('lname')
            user.email = request.form.get('email')
            user.contact = request.form.get('contact')
            user.city = request.form.get('city')
            user.image = image_name
            db.session.commit()
            msg = "Profile Updated Successfully !!"

        image_name = LoginInfo.query.filter_by(username=username).first().userref.image
        login = LoginInfo.query.filter_by(username=username).first()
        return render_template("my_profile.html",
                               message=msg,
                               errors=errors,
                               username=username,
                               image_name=image_name,
                               login=login,
                               msg=msg
                               )

    return render_template("login.html",
                           message=msg,
                           user="")


if __name__ == '__main__':
    """
    user_batches_list = LoginInfo.query.filter_by(username='amit111').first().userref.batches_list
    print(user_batches_list)

    final_batch_mates = []
    for batch in user_batches_list:
        users = batch.users_list
        for user in users:
            final_batch_mates.append(user)

    print(final_batch_mates)
    """
