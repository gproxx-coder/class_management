from models import *
from sqlalchemy import or_
import os


@app.route('/admin', methods=['GET'])
def admin_home():
    msg = ""
    if session.get('username') == "admin":
        return render_template("admin.html",
                               username=session.get('username').title())
    return render_template("login.html",
                           message=msg,
                           user="",)


############################################################################

@app.route('/admin/batch', methods=['GET'])
def batch_home():
    msg = ""
    if session.get('username') == "admin":
        batches = Batch.query.all()
        for bat in batches:
            bat.course_name = Course.query.filter_by(id=bat.course_id).first().name
        batch_search_flag = True
        batch_add_flag = False
        return render_template("batch_crud.html",
                               all_batches=batches,
                               batch=Batch.get_dummy(),
                               batch_search_flag=batch_search_flag,
                               batch_add_flag=batch_add_flag,
                               courses=Course.query.all(),
                               msg=msg,
                               username=session.get('username').title())
    return render_template("login.html",
                           message=msg,
                           user="")


@app.route('/admin/search_batch', methods=['POST'])
def search_batch():
    msg = ""
    if session.get('username') == "admin":
        batch_by_name = False
        batch_by_course = False
        found = None
        named_batches = None
        final_batches_list = []
        print("----------->", request.form.get("action"))
        if request.method == "POST":
            keyword = request.form.get("bcode")
            lookfor = f'%{keyword}%'

            if request.form.get("action").strip() == "Batch by Name":
                named_batches = Batch.query.filter(Batch.bcode.ilike(lookfor)).all()
                batch_by_name = True
                if named_batches:
                    found = f"Batches Found with keyword `{keyword}`"
                else:
                    found = f"Batches Not Found with keyword `{keyword}`"
                final_batches_list = named_batches

            elif request.form.get("action") == "Batch by Course":
                matched_courses = Course.query.filter(Course.name.ilike(lookfor)).all()
                print(matched_courses)
                final_batches_list = []
                for cor in matched_courses:
                    bat = cor.batches_list
                    # print(bat)
                    if bat:
                        for inner_bat in bat:
                            final_batches_list.append(inner_bat)

                print(final_batches_list)
                batch_by_course = True
                if final_batches_list:
                    found = f"Batches Found with Course `{keyword}`"
                else:
                    found = f"Batches Not Found with Course `{keyword}`"

        batch_search_flag = True
        batch_add_flag = False
        all_batches = Batch.query.all()
        return render_template("batch_crud.html",
                               username=session.get('username').title(),
                               all_batches=all_batches,
                               batch=Batch.get_dummy(),
                               batch_search_flag=batch_search_flag,
                               batch_add_flag=batch_add_flag,
                               named_batches=named_batches,
                               final_batches_list=final_batches_list,
                               found=found,
                               batch_by_name=batch_by_name,
                               batch_by_course=batch_by_course)
    return render_template("login.html",
                           message=msg,
                           user="")


"""
@app.route('/admin/batch_by_course', methods=['GET'])
def get_batch_by_course_name():
    found = None
    named_batches = None
    if request.method == "POST":
        keyword = request.form.get("bcode")
        lookfor = f'%{keyword}%'
        named_batches = Batch.query.filter(Batch.bcode.ilike(lookfor)).all()
        if named_batches:
            found = f"Batches Found with keyword `{keyword}`"
        else:
            found = f"Batches Not Found with keyword `{keyword}`"
        print(named_batches)
    courses = Course.query.all()
    course_search_flag = True
    course_add_flag = False
    batches = Batch.query.all()
    return render_template("course_crud.html",
                           batches=batches,
                           batch=Batch.get_dummy(),
                           batch_search_flag=course_search_flag,
                           batch_add_flag=course_add_flag,
                           named_batches=named_batches,
                           found=found)
"""


@app.route('/admin/batch/save', methods=['POST', 'GET'])
def batch_save_or_update():
    msg = ""
    if session.get('username') == "admin":
        if request.method == "POST":
            bid = request.form.get("bid")
            bcode_ = request.form.get("bcode")
            start_date = request.form.get("bdate")
            course_id = request.form.get("courses")
            print("Course ID--->", course_id)

            duplicate_bcode = Batch.query.filter_by(bcode=bcode_).first()
            batch = Batch.query.filter_by(id=bid).first()
            if duplicate_bcode:
                msg = f"Batch with Name {bcode_} Already Exists. User Other Name."
            elif batch:
                batch.bcode = bcode_
                batch.start_date = start_date
                batch.course_id = course_id
                msg = "Batch Updated Successfully"
            else:
                batch = Batch(id=bid, bcode=bcode_, start_date=start_date, course_id=course_id)
                db.session.add(batch)
                db.session.commit()
                msg = "Batch Added Successfully"

        batches = Batch.query.all()
        for bat in batches:
            bat.course_name = Course.query.filter_by(id=bat.course_id).first().name

        batch_search_flag = True
        batch_add_flag = True
        return render_template("batch_crud.html",
                               all_batches=batches,
                               batch_search_flag=batch_search_flag,
                               batch_add_flag=batch_add_flag,
                               batch=Batch.get_dummy(),
                               courses=Course.query.all(),
                               msg=msg,
                               username=session.get('username').title())
    return render_template("login.html",
                           message=msg,
                           user="")


@app.route('/admin/batch/edit/<int:bid>', methods=['GET'])
def batch_edit(bid):
    msg = ""
    if session.get('username') == "admin":
        batches = Batch.query.all()
        batch = Batch.query.filter_by(id=bid).first()
        # for bat in batches:
        #     bat.course_name = Course.query.filter_by(id=bat.course_id).first().name
        batch_search_flag = True
        batch_add_flag = True
        return render_template("batch_crud.html",
                               batches=batches,
                               batch_search_flag=batch_search_flag,
                               batch_add_flag=batch_add_flag,
                               batch=batch,
                               courses=Course.query.all(),
                               msg=msg,
                               username=session.get('username').title())
    return render_template("login.html",
                           message=msg,
                           user="")


@app.route('/admin/batch/delete/<int:bid>', methods=['GET'])
def batch_delete(bid):
    msg = ""
    if session.get('username') == "admin":
        batch = Batch.query.filter_by(id=bid).first()
        db.session.delete(batch)
        db.session.commit()
        msg = "Batch Removed Successfully"
        batches = Batch.query.all()
        for bat in batches:
            bat.course_name = Course.query.filter_by(id=bat.course_id).first().name
        return render_template("batch_crud.html",
                               batches=batches,
                               batch=Batch.get_dummy(),
                               courses=Course.query.all(),
                               msg=msg,
                               username=session.get('username').title())
    return render_template("login.html",
                           message=msg,
                           user="")


#############################################################################


#############################################################################

@app.route('/admin/course', methods=['GET'])
def course_home():
    msg = ""
    if session.get('username') == "admin":
        courses = Course.query.all()
        course_search_flag = True
        course_add_flag = False
        return render_template("course_crud.html",
                               courses=courses,
                               course=Course.get_dummy(),
                               course_search_flag=course_search_flag,
                               course_add_flag=course_add_flag,
                               username=session.get('username').title())
    return render_template("login.html",
                           message=msg,
                           user="")


@app.route('/admin/course_by_name', methods=['POST'])
def get_course_by_name():
    msg = ""
    if session.get('username') == "admin":
        found = None
        named_courses = None
        if request.method == "POST":
            keyword = request.form.get("cname")
            lookfor = f'%{keyword}%'
            named_courses = Course.query.filter(Course.name.ilike(lookfor)).all()
            if named_courses:
                found = f"Courses Found with keyword `{keyword}`"
            else:
                found = f"Courses Not Found with keyword `{keyword}`"
            print(named_courses)
        courses = Course.query.all()
        course_search_flag = True
        course_add_flag = False
        return render_template("course_crud.html",
                               courses=courses,
                               course=Course.get_dummy(),
                               course_search_flag=course_search_flag,
                               course_add_flag=course_add_flag,
                               named_courses=named_courses,
                               found=found,
                               username=session.get('username').title())
    return render_template("login.html",
                           message=msg,
                           user="")


@app.route('/admin/course/save', methods=['POST', 'GET'])
def course_save_or_update():
    msg = ""
    if session.get('username') == "admin":
        if request.method == "POST":
            cid = request.form.get("cid")
            cname = request.form.get("cname")
            fees = request.form.get("fees")
            duration = request.form.get("duration")

            course = Course.query.filter_by(id=cid).first()
            if course:
                course.name = cname
                course.fees = fees
                course.duration = duration
                db.session.commit()
                msg = "Course Updated Successfully"
            else:
                course = Course(id=cid, name=cname, fees=fees, duration=duration)
                db.session.add(course)
                db.session.commit()
                msg = "Course Added Successfully"

        courses = Course.query.all()
        course_search_flag = True
        course_add_flag = True
        return render_template("course_crud.html",
                               courses=courses,
                               course_search_flag=course_search_flag,
                               course_add_flag=course_add_flag,
                               course=Course.get_dummy(),
                               msg=msg,
                               username=session.get('username').title())
    return render_template("login.html",
                           message=msg,
                           user="")


@app.route('/admin/course/edit/<int:cid>', methods=['GET'])
def course_edit(cid):
    msg = ""
    if session.get('username') == "admin":
        course_search_flag = True
        course_add_flag = True
        courses = Course.query.all()
        course = Course.query.filter_by(id=cid).first()
        return render_template("course_crud.html",
                               courses=courses,
                               course=course,
                               course_search_flag=course_search_flag,
                               course_add_flag=course_add_flag,
                               username=session.get('username').title())
    return render_template("login.html",
                           message=msg,
                           user="")


@app.route('/admin/course/delete/<int:cid>', methods=['GET'])
def course_delete(cid):
    msg = ""
    if session.get('username') == "admin":
        course = Course.query.filter_by(id=cid).first()
        if course:
            db.session.delete(course)
            db.session.commit()
            msg = "Course Deleted Successfully"
        else:
            course = Course.get_dummy()
            msg = "Course Not Found"
        courses = Course.query.all()
        course_search_flag = True
        course_add_flag = False
        return render_template("course_crud.html",
                               courses=courses,
                               course_search_flag=course_search_flag,
                               course_add_flag=course_add_flag,
                               course=Course.get_dummy(),
                               msg=msg,
                               username=session.get('username').title())
    return render_template("login.html",
                           message=msg,
                           user="")


##############################################################################

##############################################################################

@app.route('/admin/role', methods=['GET'])
def role_home():
    msg = ""
    if session.get('username') == "admin":
        roles = Role.query.all()
        return render_template("role_crud.html",
                               roles=roles,
                               role=Role.get_dummy(),
                               username=session.get('username').title())
    return render_template("login.html",
                           message=msg,
                           user="")


@app.route('/admin/role/save', methods=['POST', 'GET'])
def role_save_or_update():
    msg = ""
    if session.get('username') == "admin":
        if request.method == "POST":
            rid = request.form.get("rid")
            role_name = request.form.get("role")

            role = Role.query.filter_by(id=rid).first()
            if role:
                role.role = role_name
                db.session.commit()
                msg = "Role Updated Successfully"
            else:
                role = Role(id=rid, role=role_name)
                db.session.add(role)
                db.session.commit()
                msg = "Role Added Successfully"

        roles = Role.query.all()
        return render_template("role_crud.html",
                               roles=roles,
                               role=Role.get_dummy(),
                               msg=msg,
                               username=session.get('username').title())
    return render_template("login.html",
                           message=msg,
                           user="")


@app.route('/admin/role/edit/<int:rid>', methods=['GET'])
def role_edit(rid):
    msg = ""
    if session.get('username') == "admin":
        roles = Role.query.all()
        role = Role.query.filter_by(id=rid).first()
        return render_template("role_crud.html",
                               roles=roles,
                               role=role,
                               username=session.get('username').title())
    return render_template("login.html",
                           message=msg,
                           user="")


@app.route('/admin/role/delete/<int:rid>', methods=['GET'])
def role_delete(rid):
    msg = ""
    if session.get('username') == "admin":
        role = Role.query.filter_by(id=rid).first()
        if role:
            db.session.delete(role)
            db.session.commit()
            msg = "Role Deleted Successfully"
        else:
            role = Role.get_dummy()
            msg = "Role Not Found"
        roles = Role.query.all()
        return render_template("role_crud.html",
                               roles=roles,
                               role=Course.get_dummy(),
                               msg=msg,
                               username=session.get('username').title())
    return render_template("login.html",
                           message=msg,
                           user="")


##############################################################################

##############################################################################

@app.route('/admin/status', methods=['GET'])
def status_home():
    msg = ""
    if session.get('username') == "admin":
        statuses = UserStatus.query.all()
        return render_template("status_crud.html",
                               statuses=statuses,
                               status=UserStatus.get_dummy(),
                               username=session.get('username').title())
    return render_template("login.html",
                           message=msg,
                           user="")


@app.route('/admin/status/save', methods=['POST'])
def status_save_or_update():
    msg = ""
    if session.get('username') == "admin":
        if request.method == "POST":
            sid = request.form.get("sid")
            sname = request.form.get("sname")

            status = UserStatus.query.filter_by(id=sid).first()
            if status:
                status.status = sname
                db.session.commit()
                msg = "Status Updated Successfully"
            else:
                status = UserStatus(id=sid, status=sname)
                db.session.add(status)
                db.session.commit()
                msg = "Status Added Successfully"

        statuses = UserStatus.query.all()
        return render_template("status_crud.html",
                               statuses=statuses,
                               status=Role.get_dummy(),
                               msg=msg,
                               username=session.get('username').title())
    return render_template("login.html",
                           message=msg,
                           user="")


@app.route('/admin/status/edit/<int:sid>', methods=['GET'])
def status_edit(sid):
    msg = ""
    if session.get('username') == "admin":
        status = UserStatus.query.filter_by(id=sid).first()
        statuses = UserStatus.query.all()
        return render_template("status_crud.html",
                               statuses=statuses,
                               status=status,
                               username=session.get('username').title())
    return render_template("login.html",
                           message=msg,
                           user="")


@app.route('/admin/status/delete/<int:sid>', methods=['GET'])
def status_delete(sid):
    msg = ""
    if session.get('username') == "admin":
        status = UserStatus.query.filter_by(id=sid).first()
        if status:
            db.session.delete(status)
            db.session.commit()
            msg = "Status Deleted Successfully"
        else:
            status = UserStatus.get_dummy()
            msg = "Status Not Found"
        statuses = UserStatus.query.all()
        return render_template("status_crud.html",
                               statuses=statuses,
                               status=UserStatus.get_dummy(),
                               msg=msg,
                               username=session.get('username').title())
    return render_template("login.html",
                           message=msg,
                           user="")


##############################################################################

##############################################################################

@app.route('/admin/user', methods=['GET'])
def user_home():
    msg = ""
    if session.get('username') == "admin":
        if request.method == "POST":
            pass
        logins = LoginInfo.query.all()
        batches = Batch.query.all()
        user_search_flag = True
        user_add_flag = False
        return render_template("user_crud.html",
                               logins=logins,
                               login=LoginInfo.get_dummy(),
                               user_search_flag=user_search_flag,
                               user_add_flag=user_add_flag,
                               batches=batches,
                               msg=msg,
                               username=session.get('username').title())
    return render_template("login.html",
                           message=msg,
                           user="")


@app.route('/admin/search_user', methods=['POST'])
def search_user():
    msg = ""
    if session.get('username') == "admin":
        user_by_name = False
        user_by_username = False
        user_by_batch = False
        user_by_status = False
        user_by_role = False
        keyword = ""
        found1 = None
        found2 = None
        named_users = None
        final_users_list = []
        final_username_list = []

        print("----------->", request.form.get("action"))
        if request.method == "POST":
            keyword = request.form.get("name")
            lookfor = f'%{keyword}%'

            # Find User by First or Last Names
            if request.form.get("action").strip() == "User by Name":
                user_results = UserInfo.query.filter(or_(UserInfo.fname.ilike(lookfor),
                                                         UserInfo.lname.ilike(lookfor))).all()
                for user in user_results:
                    if user.loginref:
                        final_users_list.append(user)
                if user_results:
                    found1 = f"Users Found with keyword `{keyword}`"
                else:
                    found1 = f"Users Not Found with keyword `{keyword}`"

                user_by_name = True

            # Find User by Usernames
            elif request.form.get("action") == "User by Username":

                matched_usernames = LoginInfo.query.filter(LoginInfo.username.ilike(lookfor)).all()
                print(matched_usernames)
                final_username_list = matched_usernames

                if final_username_list:
                    user_by_username = True
                    found2 = f"Users Found contains Username `{keyword}`"
                else:
                    found2 = f"Users Not Found contains Username `{keyword}`"

            # Find User by Batch
            elif request.form.get("action") == "User by Batch":

                lookfor = request.form.get("name")
                matched_batches = UserInfo.query.all()
                final_user_batch_list = []
                for user in matched_batches:
                    for bat in user.batches_list:
                        if lookfor.lower() in bat.bcode.lower():
                            final_user_batch_list.append(user)

                final_users_list = final_user_batch_list

                if final_users_list:
                    user_by_batch = True
                    found1 = f"Users Found from Batch `{keyword}`"
                else:
                    found1 = f"Users Not Found from Batch `{keyword}`"

            # Find User by Status
            elif request.form.get("action") == "User by Status":

                final_login_status_list = []
                lookfor = request.form.get("name")
                logins = LoginInfo.query.all()
                for logg in logins:
                    sta = logg.statusref.status.lower()
                    if lookfor.lower() in sta:
                        final_login_status_list.append(logg)

                print(final_login_status_list)
                final_username_list = final_login_status_list
                if final_username_list:
                    user_by_status = True
                    found2 = f"Users Found Status Containing `{keyword}`"
                else:
                    found2 = f"Users Not Found Status Containing `{keyword}`"

            elif request.form.get("action") == "User by Role":

                final_login_role_list = []
                lookfor = request.form.get("name")
                logins = LoginInfo.query.all()
                for logg in logins:
                    rol = logg.roleref.role.lower()
                    if lookfor.lower() in rol:
                        final_login_role_list.append(logg)

                print(final_login_role_list)
                final_username_list = final_login_role_list

                if final_username_list:
                    user_by_role = True
                    found2 = f"Users Found Role Containing `{keyword}`"
                else:
                    found2 = f"Users Not Found Role Containing `{keyword}`"

        user_search_flag = True
        user_add_flag = False
        all_batches = Batch.query.all()
        logins = LoginInfo.query.all()
        return render_template("user_crud.html",
                               login=LoginInfo.get_dummy(),
                               logins=logins,
                               all_batches=all_batches,
                               batch=Batch.get_dummy(),
                               user_search_flag=user_search_flag,
                               user_add_flag=user_add_flag,
                               named_batches=named_users,
                               final_users_list=final_users_list,
                               final_username_list=final_username_list,
                               found1=found1,
                               found2=found2,
                               user_by_name=user_by_name,
                               user_by_username=user_by_username,
                               user_by_batch=user_by_batch,
                               user_by_role=user_by_role,
                               user_by_status=user_by_status,
                               keyword=keyword,
                               username=session.get('username').title()
                               )
    return render_template("login.html",
                           message=msg,
                           user="")


@app.route('/admin/user/save', methods=['POST', 'GET'])
def user_save_or_update():
    """
    Admin can only change Contact Number & Batches in this function.
    """
    msg = ""
    if session.get('username') == "admin":
        if request.method == "POST":
            user_contact = request.form.get("contact")
            user_batches = request.form.getlist("batches")
            user_id = request.form.get("uid")
            user_object = UserInfo.query.filter_by(id=user_id).first()
            new_status = request.form.get("new_status")
            new_role = request.form.get("new_role")
            print("New Status----->", new_status)
            print("New Role----->", new_role)
            print("Batches List------>", user_batches)
            print("User Object------>", user_object)

            login_object = user_object.loginref

            login_object.user_status = new_status
            login_object.user_role = new_role
            db.session.commit()

            # Updating User Contact No
            user_object.contact = user_contact
            db.session.commit()

            # Adding batches to user
            for bid in user_batches:
                batch = Batch.query.filter_by(id=bid).first()
                user_object.batches_list.append(batch)

            msg = "User Updated Successfully"

            db.session.commit()
            # msg = "Status Added Successfully"
            user_add_flag = False
        logins = LoginInfo.query.all()
        batches = Batch.query.all()
        user_search_flag = True
        user_add_flag = False
        return render_template("user_crud.html",
                               user=UserInfo.get_dummy(),
                               logins=logins,
                               user_search_flag=user_search_flag,
                               user_add_flag=user_add_flag,
                               login=LoginInfo.get_dummy(),
                               batches=batches,
                               msg=msg,
                               username=session.get('username').title())
    return render_template("login.html",
                           message=msg,
                           user="",
                           user_add_flag=False)


@app.route("/admin/user/batch/delete/<int:uid>/<int:bid>")
def user_batch_delete(uid, bid):
    msg = ""
    if session.get('username') == "admin":
        user_contact = request.form.get("contact")
        user_batches = request.form.getlist("batches")

        user_id = uid

        print(user_id)

        user_object = UserInfo.query.filter_by(id=user_id).first()

        print("Batches LIST---->", user_object.batches_list)

        user_object.batches_list.remove(Batch.query.filter_by(id=bid).first())

        db.session.commit()

        # login = LoginInfo.query.filter_by(id=bid).first()
        logins = LoginInfo.query.all()
        batches = Batch.query.all()
        user_search_flag = True
        user_add_flag = False
        return render_template("user_crud.html",
                               logins=logins,
                               login=LoginInfo.get_dummy(),
                               user_search_flag=user_search_flag,
                               user_add_flag=user_add_flag,
                               batches=batches,
                               msg=msg,
                               username=session.get('username').title())
    return render_template("login.html",
                           message=msg,
                           user="",
                           user_add_flag=False)


@app.route('/admin/user/edit/<int:sid>', methods=['GET'])
def user_edit(sid):
    msg = ""
    if session.get('username') == "admin":
        login = LoginInfo.query.filter_by(id=sid).first()
        logins = LoginInfo.query.all()
        batches = Batch.query.all()
        user_search_flag = True
        user_add_flag = True
        all_statuses = UserStatus.query.all()
        all_roles = Role.query.all()
        return render_template("user_crud.html",
                               logins=logins,
                               user_search_flag=user_search_flag,
                               user_add_flag=user_add_flag,
                               login=login,
                               batches=batches,
                               msg=msg,
                               username=session.get('username').title(),
                               all_statuses=all_statuses,
                               all_roles=all_roles)
    return render_template("login.html",
                           message=msg,
                           user="")


@app.route('/admin/user/delete/<int:sid>', methods=['GET'])
def user_delete(sid):
    msg = ""
    if session.get('username') == "admin":
        login = LoginInfo.query.filter_by(id=sid).first()
        user = login.userref
        image_name = ""
        if login:
            image_name = login.userref.image
            db.session.delete(login)
            db.session.delete(user)
            db.session.commit()

        cwd = os.getcwd()
        img_path = cwd + "/" + "static/" + image_name
        print("IMAGE_PATH--->", img_path)
        try:
            os.remove(img_path)
        except BaseException as e:
            print(e)

        logins = LoginInfo.query.all()
        batches = Batch.query.all()
        user_search_flag = True
        user_add_flag = False
        return render_template("user_crud.html",
                               logins=logins,
                               user_search_flag=user_search_flag,
                               user_add_flag=user_add_flag,
                               login=LoginInfo.get_dummy(),
                               batches=batches,
                               msg=msg,
                               username=session.get('username').title())
    return render_template("login.html",
                           message=msg,
                           user="")


##############################################################################


if __name__ == '__main__':
    pass
    """
    # Final User List------ SEARCH BY NAME
    final_users_list = []
    lookfor = "%ga%"
    # logins = LoginInfo.query.all()
    # for logg in logins:
    #     print(logg.userref.fname + " " + logg.userref.lname)

    user_results = UserInfo.query.filter(or_(UserInfo.fname.ilike(lookfor), UserInfo.lname.ilike(lookfor))).all()
    # print(user_results)

    for user in user_results:
        if user.loginref:
            final_users_list.append(user)

    print(final_users_list)
    """

    """
    final_login_status_list = []
    lookfor = "blo"
    logins = LoginInfo.query.all()
    for logg in logins:
        sta = logg.statusref.status.lower()
        if lookfor.lower() in sta:
            final_login_status_list.append(logg)

    print(final_login_status_list)"""

    # user_results = UserInfo.query.filter(or_(UserInfo.fname.ilike(lookfor), UserInfo.lname.ilike(lookfor))).all()
    # print(user_results)

    """
    users_batches = []
    lookfor = "13"

    matched_batches = UserInfo.query.all()
    final_user_batch_list = []
    for user in matched_batches:
        for bat in user.batches_list:
            if lookfor in bat.bcode:
                final_user_batch_list.append(user)"""

"""
    final_userinfo_list = []
    lookfor = "%11%"
    matched_usernames = LoginInfo.query.filter(LoginInfo.username.ilike(lookfor)).all()
    print(matched_usernames)

    for logg in matched_usernames:
        print(logg.userref.id)
        print(logg.userref.fname, logg.userref.lname)
        print(logg.userref.email)
        print(logg.statusref.status)
        print(logg.roleref.role)
        print("-------------")
"""

# result = LoginInfo.query.filter(LoginInfo.userref.name.ilike(lookfor)).all()
# print(result)

"""
    matched_courses = Course.query.filter(Course.name.ilike('%pyt%')).all()
    # print(matched_courses)
    final_batches_list = []
    for cor in matched_courses:
        bat = cor.batches_list
        # print(bat)
        if bat:
            for inner_bat in bat:
                final_batches_list.append(inner_bat)

    # print(final_batches_list)

    for bat in final_batches_list:
        print("---------", bat)
        # print(bat.id)
        # print(bat.bcode)
        # print(bat.startdate)
        # print(bat.courseref)
"""
# batch = Batch.query.filter_by(id=502).first()
# print(batch)
# print(Course.query.filter_by(id=batch.course_id).first().name)

# usr = UserInfo(id=100, fname="Ganesh", lname="Patil", email="admin@admin.com", contact="9130427302", city="Pune", gender="male", image="")
# db.session.add(usr)
# db.session.commit()

# login = LoginInfo(id=1,
#                   username="admin",
#                   password="8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918",
#                   user_id=100, user_status=10, user_role=500)
#
# db.session.add(login)
# db.session.commit()
