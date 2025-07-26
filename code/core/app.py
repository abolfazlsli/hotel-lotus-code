from flask import *
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from flask import session, redirect
import os 
import string , random
from datetime import datetime


app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.secret_key = "acnascnnvfedklvfdjkvnslvnsdnvdsvnsdk;vn;kd"

db = SQLAlchemy(app)


def generateDigitalIds():
    prefix = "DIG"
    date_part = datetime.now().strftime("%Y%m%d")
    random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"{prefix}-{date_part}-{random_part}"

class FileManager(db.Model):
    __tablename__ = 'file_manager'
    
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    fileid = db.Column(db.String(100), nullable=False)

    def __init__(self, filename, fileid):
        self.filename = filename
        self.fileid = fileid

class Room(db.Model):
    __tablename__ = 'rooms'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    imageid = db.Column(db.String(100), nullable=True)
    caption = db.Column(db.Text, nullable=True)

    def __init__(self, name, imageid, caption):
        self.name = name
        self.imageid = imageid
        self.caption = caption

class Options(db.Model):
    __tablename__ = 'options'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    imageid = db.Column(db.String(100), nullable=True)
    caption = db.Column(db.Text, nullable=True)

    def __init__(self, name, imageid, caption):
        self.name = name
        self.imageid = imageid
        self.caption = caption


class LandingsPhone(db.Model):
    __tablename__ = "landingphone"
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String)
    def __init__(self , phone):
        self.phone = phone

class LandingAddres(db.Model):
    __tablename__ = "landingaddres"
    id = db.Column(db.Integer, primary_key=True)
    addres = db .Column(db.String)
    def __init__(self , addres):
        self.addres = addres



class Admins(db.Model):
    __tablename__ = 'admins'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __init__(self, name, phone, password):
        self.name = name
        self.phone = phone
        self.password = password


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "admin_id" not in session:
            return redirect("/admin/login")
        return f(*args, **kwargs)
    return decorated_function


@app.route("/admin")
@login_required
def adminhome () :
    return redirect("/admin/dashboard")


@app.route("/admin/addresadder" , methods = ["GET" , "POST"])
@login_required
def addAdres () :
    if request.method == "GET" :
        return render_template("/addresAdder.html")
    elif request.method == "POST" :
        try:
            addres = request.form.get("addres")
            ad = LandingAddres(addres)
            db.session.add(ad)
            db.session.commit()
            return render_template("/addresAdder.html" , message = "address added !")
        except :
            return render_template("/addresAdder.html" , error = "Cant add address !")
    return ""

@app.route("/admin/delphone/<id>" , methods = ["GET" , "POST"])
@login_required
def remphone(id):
    phone = LandingsPhone.query.filter_by(id = id)
    phone.delete()
    db.session.commit()
    return redirect("/admin/dashboard")



@app.route("/admin/editbanner", methods=["GET", "POST"])
@login_required
def EditBanner():
    if request.method == "GET":
        return render_template("editcover.html")
    elif request.method == "POST":
        file = request.files.get("banner")
        if file:
            assets_folder = os.path.join(current_app.root_path, "static", "assets")
            if not os.path.exists(assets_folder):
                os.makedirs(assets_folder)
            file.save(os.path.join(assets_folder, "mainimage.png"))
            return redirect("/admin/editbanner")
    return ""

@app.route("/admin/deladdres/<id>" , methods = ["GET" , "POST"])
@login_required
def remaddres(id):
    phone = LandingAddres.query.filter_by(id = id)
    phone.delete()
    db.session.commit()
    return redirect("/admin/dashboard")

@app.route("/admin/phoneadder" , methods=["GET" , 'POST'])
@login_required
def addPhone () :
    if request.method == "GET":
        return render_template("addingphone.html")
    elif request.method == "POST":
        try:
            phone = LandingsPhone(request.form.get("phone"))
            db.session.add(phone)
            db.session.commit()
            return render_template("addingphone.html" , message="adding phone sucess !")
        except:
            return render_template("addingphone.html" , error = "we have a problem in adding phone !")
    return ""

@app.route("/admin/addoption", methods=["GET", "POST"])
@login_required
def addoption():
    if request.method == "POST":
        name = request.form.get("name")
        file = request.files.get("imageid")
        caption = request.form.get("caption")
        digtitalfilename = generateDigitalIds()
        filefild = FileManager(file.filename , digtitalfilename)
        db.session.add(filefild)
        db.session.commit()
        file.save(f"./static/pics/{digtitalfilename}.{file.filename.split(".")[-1]}")
        if not name:
            return render_template("addoption.html", error="Option name is required.")

        try:
            new_option = Options(name=name, imageid=f"{digtitalfilename}.{file.filename.split(".")[-1]}", caption=caption)
            db.session.add(new_option)
            db.session.commit()
            return render_template("addoption.html", message="Option added successfully!")
        except Exception as e:
            return render_template("addoption.html", error="Database error: " + str(e))

    return render_template("addoption.html")



@app.route("/admin/addroom", methods=["GET", "POST"])
@login_required
def addroom():
    if request.method == "POST":
        name = request.form.get("name")
        caption = request.form.get("caption")
        file = request.files.get("imageid")
        digtitalfilename = generateDigitalIds()
        filefild = FileManager(file.filename , digtitalfilename)
        db.session.add(filefild)
        db.session.commit()
        file.save(f"./static/pics/{digtitalfilename}.{file.filename.split(".")[-1]}")
        if not name:
            return render_template("addroom.html", error="Room name is required.")
        try:
            new_room = Room(name=name, imageid=f"{digtitalfilename}.{file.filename.split(".")[-1]}", caption=caption)
            db.session.add(new_room)
            db.session.commit()
            return render_template("addroom.html", message="Room added successfully!")
        except Exception as e:
            return render_template("addroom.html", error="Database error: " + str(e))

    return render_template("addroom.html")




@app.route("/admin/option/delete/<oid>")
@login_required
def deloption(oid):
    option = Options.query.filter_by(id = oid)
    try:
        os.remove("./static/pics/" + option.first().imageid)
    except:
        pass
    option.delete()
    db.session.commit()
    return redirect("/admin/dashboard")

@app.route("/admin/room/edit/<oid>" , methods = ['POST' , 'GET'])
@login_required
def editroom(oid):
    if request.method == "POST":
        data = request.form
        files = request.files
        room = Room.query.filter_by(id = oid)
        newImageID = generateDigitalIds()
        room.first().name = data.get("name")
        room.first().caption = data.get("caption")
        files.get("imageid").save("./static/pics" + f"{newImageID}.{files.get("imageid").filename.split(".")[-1]}")
        # os.remove("./static/pic/" + room.first().imageid)
        room.first().imageid = f"{newImageID}.{files.get("imageid").filename.split(".")[-1]}"
        db.session.commit()
        return redirect("/admin/dashboard")
    else:
        data = Room.query.filter_by(id = oid)
        return render_template("editroom.html" , data = data)


@app.route("/admin/option/edit/<oid>", methods=['GET', 'POST'])
@login_required
def editoption(oid):
    if request.method == "POST":
        data = request.form
        files = request.files
        option = Options.query.filter_by(id=oid)
        new_image_id = generateDigitalIds()

        option.first().name = data.get("name")
        option.first().caption = data.get("caption")

        if files.get("imageid") and files.get("imageid").filename != "":
            ext = files.get("imageid").filename.split(".")[-1]
            new_filename = f"{new_image_id}.{ext}"
            files.get("imageid").save(f"./static/pics/{new_filename}")
            
            try:
                os.remove(f"./static/pics/{option.first().imageid}")
            except:
                pass

            option.first().imageid = new_filename

        db.session.commit()
        return redirect("/admin/dashboard")

    else:
        data = Options.query.filter_by(id=oid)
        return render_template("editoption.html", data=data)



@app.route("/admin/room/delete/<oid>")
@login_required
def delroom(oid):
    option = Room.query.filter_by(id = oid)
    try:
        os.remove("./static/pics/" + option.first().imageid)
    except:
        pass
    option.delete()
    db.session.commit()
    return redirect("/admin/dashboard")


@app.route("/admin/dashboard")
@login_required
def dashboard():
    rooms = Room.query.all()
    options = Options.query.all()
    phones = LandingsPhone.query.all()
    address = LandingAddres.query.all()
    return render_template("dashboard.html", rooms=rooms, options=options , phones=phones , address = address , str=str)




@app.route("/image/<fileid>")
def serve_image(fileid):
    file = FileManager.query.filter_by(fileid=fileid).first()
    if file:
        path = os.path.join("uploads", file.filename)
        return send_file(path, mimetype="image/jpeg")
    return "Image not found", 404


@app.route("/admin/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        phone = request.form.get("phone")
        password = request.form.get("password")
        admin = Admins.query.filter_by(phone=phone, password=password).first()
        if admin:
            session["admin_id"] = admin.id
            session["admin_name"] = admin.name
            return redirect("/admin/dashboard")
        return "Login failed"
    
    return render_template("login.html")


@app.route("/setupadmin" , methods = ["GET" , "POST"])
def setupAddmin () :
    if request.method == "GET" :
        return render_template("createRoot.html")
    else : 
        data = request.form
        admin = Admins(data.get("phone") , data.get("phone") , data.get("password"))
        db.session.add(admin)
        db.session.commit()
        return redirect("/admin")



@app.route("/admin/logout")
@login_required
def logout() :
    session.clear()
    return redirect("/")

@app.route("/")
def homePage () :
    rooms =Room.query.all()
    options = Options.query.all()
    phones = LandingsPhone.query.all()
    addr = LandingAddres.query.all()
    return render_template("index.html" , rooms = rooms , options = options , phones = phones , address = addr)

with app.app_context():
    db.create_all()






if __name__ == "__main__":
    app.run(debug=True , port=80 , host="0.0.0.0")
