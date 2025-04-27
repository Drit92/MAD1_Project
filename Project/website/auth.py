from flask import Blueprint, render_template, request, redirect, url_for
from .models import User,Song,Playlist,Review, association,Album
from flask import current_app 
from . import db
import os
from . import create_app
from datetime import datetime 


auth = Blueprint('auth', __name__)





@auth.route('/admin_login', methods=['GET','POST'])
def adlog():
    if request.method == 'POST':
        username0 = request.form.get('username0')
        password0 = request.form.get('password0')
        if username0=="Admin_user":
            if password0=="1234Admin":
                us_no=len(User.query.all())
                solist=Song.query.all()
                albums=Album.query.all()
                block_no=len(User.query.filter_by(user_status="Blocked").all())
                son_details=url_for('views.songttdts',songs=solist)
                
                
                return render_template("Adpage.html",us_no=us_no,song_no=len(solist),album_no=len(albums),block_no=block_no, solist=solist,albums=albums,son_details=son_details)
    
    return render_template("AdminLogin.html")



@auth.route('/user_login', methods=['GET','POST'])
def uslog():
    mssg=None
    
    if request.method == 'POST':
        username2 = request.form.get('username2')
        password2 = request.form.get('password2')
        
        user = User.query.filter_by(user_name=username2).first()
        if user:
            if user.user_password == password2 :
                ustat= user.user_status 
                uid = user.user_id
                if ustat=="blocked":
                    print(ustat)
                    mssg = "Your Account has been blocked by the admin"
                    return render_template("userlogin.html",mssg=mssg)
                    
                return redirect(url_for('views.soP',ustat=ustat,uid=uid))
            else:
                mssg = "Incorrect password, try again."
        else:
            mssg ="Username does not exist."
            return render_template("userlogin.html",mssg=mssg)
    return render_template("userlogin.html",mssg=mssg)

@auth.route('/user_signup', methods=['GET','POST'])
def usinup():
    mssg=None
    
    if request.method == 'POST':
        username1 = request.form.get('username1')
        password1 = request.form.get('password1')

        

        if len(username1) < 3 :
            mssg="Username must be greater than 2 characters"
        elif len(password1) < 6:
            mssg="Password must be at least 6 characters."
        elif bool(User.query.filter_by(user_name=username1).first()):
            mssg="Username already exists. Choose another username"
            #return redirect('/user_signup')
        else:
            
            new_user = User(user_name=username1, user_password=password1,user_status="normal")
            db.session.add(new_user)
            db.session.commit()
            uid=new_user.user_id
            ustat="normal"
            
            return redirect(url_for('views.soP',ustat=ustat,uid=uid))


    return render_template("usersignup.html",mssg=mssg)

@auth.route('/logout', methods=['GET','POST'])
def logout():       
    return redirect(url_for('views.home'))




##################


from werkzeug.utils import secure_filename



ALLOWED_EXTENSIONS = {'mp3', 'ogg', 'wav'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS







@auth.route('/<ustat>-<uid>-adsongs', methods=['GET','POST'])
def upload_file(ustat,uid):
    ustat=ustat
    uid=uid
    
    songs=None
    #UPLOAD_FOLDER=os.path.dirname(os.path.dirname(os.path.abspath('uploads')))
    UPLOAD_FOLDER='./website/static'
    current_app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
    #os.makedirs(UPLOAD_FOLDER,exist_ok=True)

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
        
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join("./website/static", filename))
            #file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

            sname = request.form['sname']
            
            saname = request.form['saname']
            

            pathe=str("../static/"+filename)
            delpathe=str("website/static/"+filename)
            date_time=str(datetime.now())

            t1=Song(song_title=sname,song_path=pathe,song_artist=saname,song_del_path=delpathe,song_datetime=date_time,total_point=0,total_revs=0)
            db.session.add(t1)
            db.session.commit()
            songs=Song.query.all()
            return render_template("Adson.html",songs=songs,ustat=ustat,uid=uid)
    songs=Song.query.all()
    return render_template("Adson.html",songs=songs,ustat=ustat,uid=uid)



@auth.route('/<ustat>-<uid>-delsongs',methods=['POST','GET'])
def delso(ustat,uid):
    solist=Song.query.all()
    if request.method == 'POST':
        toDe = request.form['soname']
        toDe = toDe
        s1=Song.query.filter_by(song_title=toDe).first()
        

        os.remove(s1.song_del_path)
        Song.query.filter_by(song_title=toDe).delete(synchronize_session='auto')
        db.session.delete(s1)

        db.session.commit()
        solist=Song.query.all()
        return render_template("Del_son.html", solist=solist,ustat=ustat,uid=uid)

    return render_template("Del_son.html", solist=solist,ustat=ustat,uid=uid)


#Add albums
@auth.route('<ustat>-<uid>/add_albums', methods=['GET','POST'])
def adbum(ustat,uid):
    albums=Album.query.all()
    ustat=ustat
    uid=uid
    if request.method == 'POST':
        alname = request.form['alname']
        agen=request.form['agen']
        al1=Album(song_artist=alname,album_genere=agen)
        db.session.add(al1)
        db.session.commit()
        albums=Album.query.all()
        return render_template("Ad_album.html",albums=albums,ustat=ustat,uid=uid)
    return render_template("Ad_album.html",albums=albums,ustat=ustat,uid=uid)

# Delete Albums
@auth.route('<ustat>-<uid>/del_albums', methods=['GET','POST'])
def delbum(ustat,uid):
    ustat=ustat
    uid=uid
    albums=Album.query.all()
    if request.method == 'POST':
        alname = request.form.get('alname')
        al1=Album.query.filter_by(song_artist=alname).first()
        db.session.delete(al1)
        db.session.commit()
        albums=Album.query.all()
        return render_template("Ad_delalbum.html",albums=albums,ustat=ustat,uid=uid)
    return render_template("Ad_delalbum.html",albums=albums,ustat=ustat,uid=uid)

@auth.route('/block',methods=['GET','POST'])
def blok():
    unormlist=User.query.filter_by(user_status="normal").all()
    crealist=User.query.filter_by(user_status="creator").all()
    blist=unormlist+crealist
    if request.method == 'POST':
        bname= request.form.get('bname')
        u1=User.query.filter_by(user_name=bname).first()
        u1.user_status="blocked"
        db.session.commit()
        unormlist=User.query.filter_by(user_status="normal").all()
        crealist=User.query.filter_by(user_status="creator").all()
        blist=unormlist+crealist
        return render_template("Block.html",blist=blist)
    return render_template("Block.html",blist=blist)

@auth.route('/blocked_list',methods=['GET','POST'])
def bloklist():
    bl=User.query.filter_by(user_status="blocked").all()
    return render_template("Blocked_list.html",bl=bl)

@auth.route('/unblock',methods=['GET','POST'])
def ublok():
    ulist=User.query.filter_by(user_status="blocked").all()
    
    if request.method == 'POST':
        bname= request.form.get('bname')
        u1=User.query.filter_by(user_name=bname).first()
        u1.user_status="normal"
        db.session.commit()
        ulist=User.query.filter_by(user_status="blocked").all()
        return render_template("Unblock.html",ulist=ulist)
    return render_template("Unblock.html",ulist=ulist)



    







        



        

