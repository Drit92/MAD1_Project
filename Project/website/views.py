from flask import Blueprint, render_template,request,redirect, url_for
from . import db
from .models import User,Song,Playlist,Review,Album
import os 


views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("landing.html")



@views.route('/admin-0-adpage')
def hadp():
    us_no=len(User.query.all())
    solist=Song.query.all()
    albums=Album.query.all()
    block_no=len(User.query.filter_by(user_status="Blocked").all())
    son_details=url_for('views.songttdts',songs=solist)             
    return render_template("Adpage.html",us_no=us_no,song_no=len(solist),album_no=len(albums),block_no=block_no, solist=solist,albums=albums,son_details=son_details)

@views.route('/details')
def songttdts():
    songs=Song.query.all()
    return render_template("A_viewsong.html",songs=songs)
    

#SongPage
@views.route('/<ustat>/<uid>', methods=['GET','POST'])
def soP(ustat,uid):
    solist=Song.query.all()
    ablist=Album.query.all()
    plist=Playlist.query.filter_by(user_id=uid).all()
    
    
    ustat=ustat
    uid=uid

    

    return render_template("SongPage.html",solist=solist,ablist=ablist,plist=plist,ustat=ustat,uid=uid)



 #UserPlaylist Page   #Create/Add
@views.route('/<ustat>/<uid>/playlists', methods=['GET','POST']) 
def usplaylist(ustat,uid):
    ustat=ustat
    uid=uid
    
    mssg=None
    if request.method == 'POST':
        newpl=request.form['newpl']
        newplson=request.form['newplson']
        p1=Playlist.query.filter_by(playlist_name=newpl,user_id=uid).first()
        s1=Song.query.filter_by(song_title=newplson).first()
        
        if bool(p1):
            if bool(s1):
                p1.members.append(s1)
                db.session.commit()

                
            else:

                
                mssg="Song not found"
        else:
            
            p1=Playlist(playlist_name=newpl,user_id=uid)
            db.session.add(p1)
            db.session.commit()
            plist=Playlist.query.filter_by(user_id=uid).all()
            if bool(s1):
                p1.members.append(s1)
                db.session.commit()
            else:
                mssg="Song not found"

        
                     
    plist=Playlist.query.filter_by(user_id=uid).all()
    return render_template("UserPlaylist.html",mssg=mssg,plist=plist,ustat=ustat,uid=uid)



#diplay AlbumsList
@views.route('/Albums_listpage')
def plistv():
    ablist= Album.query.all()

    
    return render_template("Albums_view.html",ablist=ablist)

#display Particular Album
@views.route('/Albums/<abid>')
def goto(abid):
    abe=Album.query.filter_by(album_id=abid).first()

    return render_template("Album_songs.html",abe=abe)

@views.route('/Playlists/<pid>')
def gotop(pid):
    abe=Playlist.query.filter_by(playlist_id=pid).first()

    return render_template("Playlist_songs.html",abe=abe)

#Registor Creator
@views.route('/<uid>/registor_as_creator', methods=['GET','POST'])
def rec(uid):
    mssg=None
    if request.method == 'POST':
        Val=str(request.form['reg'])
        u1=User.query.filter_by(user_id=uid).first()
        if Val=="Yes":
            
            u1.user_status="creator"
            db.session.commit()
            ustat=u1.user_status
            
        if Val=="No":
            ustat=u1.user_status
            
        solist=Song.query.all()
        ablist=Album.query.all()
        plist=Playlist.query.filter_by(user_id=uid)
        return render_template("SongPage.html",ustat=ustat,uid=uid,solist=solist,ablist=ablist,plist=plist)
    return render_template("Registor_creator.html",mssg=uid)


@views.route('/creator/<uid>/creatorpage',methods=['GET'])
def fre(uid):
    uid=uid
    ustat="creator"
    plist=Playlist.query.filter_by(user_id=uid).all()
    ablist=Album.query.all()
    slist=Song.query.all()
    ad_al=url_for('auth.adbum',ustat=ustat,uid=uid)
    del_al=url_for('auth.delbum',ustat=ustat,uid=uid)
    return render_template("CreatorPage.html",uid=uid,ustat=ustat,plist=plist,ablist=ablist,slist=slist,ad_al=ad_al,del_al=del_al)

#delete playlists
@views.route('/<ustat>/<uid>/delplaylists', methods=['GET','POST'])
def deplay(ustat,uid):
    ustat=ustat
    uid=uid
    plist=Playlist.query.filter_by(user_id=uid).all()
    
    if request.method == 'POST':
        newpl=request.form.get('newpl')
        
        p1=Playlist.query.filter_by(playlist_name=newpl,user_id=uid).first()
        db.session.delete(p1)
        db.session.commit()
            
            
        plist=Playlist.query.filter_by(user_id=uid).all()
        return render_template("UserDelPlaylist.html",plist=plist,ustat=ustat,uid=uid)
    return render_template("UserDelPlaylist.html",plist=plist,ustat=ustat,uid=uid)

@views.route('/<ustat>-<uid>-<sid>/review', methods=['GET','POST'])
def rev(uid,sid,ustat):
    uid=uid
    sid=sid
    ustat=ustat
    if request.method == 'POST':
        revw=request.form.get('revw')
        r1=Review(user_id=uid,song_id=sid,review=revw)
        db.session.add(r1)
        s1=Song.query.filter_by(song_id=sid).first()
        s1.total_point=s1.total_point+int(revw)
        s1.total_revs+=1
        s1.song_avg_review=s1.total_point/s1.total_revs
        db.session.commit()
        solist=Song.query.all()
        ablist=Album.query.all()
        plist=Playlist.query.filter_by(user_id=uid)        
        return render_template("SongPage.html",ustat=ustat,uid=uid,solist=solist,ablist=ablist,plist=plist)
        
    return render_template("Reviews.html",uid=uid,sid=sid)

@views.route('/song_lyrics/<sid>', methods=['GET'])
def spaw(sid):
    sid=sid
    song=Song.query.filter_by(song_id=sid).first()
    return render_template("Lyrics.html",song=song,sid=sid)

@views.route('/song_lyrics-<sid>-add', methods=['GET','POST'])
def der(sid):
    sid=sid
    
    song=Song.query.filter_by(song_id=sid).first()
    if request.method == 'POST':
        song=Song.query.filter_by(song_id=sid).first()
        lyric=request.form['lyric']
        song.song_lyrics= lyric
        db.session.commit()    
        return redirect(url_for('auth.upload_file')) 
    place=song.song_lyrics  


    return render_template("AdLyrics.html",sid=sid,place=place)

@views.route('/search', methods=['GET','POST'])
def seeee():
    foundSong=None
    foundAlbum=None
    foundArtist=None
    mssg="No matches"
    if request.method == 'POST':
        worrd=request.form['worrd']
        foundSong=Song.query.filter_by(song_title=worrd).first()
        foundArtist=Song.query.filter_by(song_artist=worrd).all()
        foundAlbum=Album.query.filter_by(song_artist=worrd).first()
        
        if foundSong or foundAlbum:
            mssg=None
        return render_template("Search.html",foundSong=foundSong,foundAlbum=foundAlbum,foundArtist=foundArtist,mssg=mssg)
    return render_template("Search.html",foundSong=foundSong,foundAlbum=foundAlbum,foundArtist=foundArtist,mssg=mssg)

#Trending songs
@views.route('/<ustat>-<uid>trending')
def trendsi(ustat,uid):
    ustat=ustat
    uid=uid
    
    sbest=Song.query.order_by(Song.song_avg_review.desc()).limit(10).all()
    slate=Song.query.order_by(Song.song_datetime.desc()).limit(10).all()
    return render_template("Trend.html",sbest=sbest,slate=slate,ustat=ustat,uid=uid)


@views.route('/<ustat>-<uid>-edit', methods=['GET','POST'])
def editingh(ustat,uid):
    
    ustat=ustat
    uid=uid
    ename=None
    eart=None
    solist=[]
    if request.method == 'POST':
        soname=str(request.form['soname'])
        newsoname=str(request.form['newsoname'])
        newart=str(request.form['newart'])

        esong=Song.query.filter_by(song_title=soname).first()
        ename=esong.song_title
        eart=esong.song_artist

        if eart==None:
            eart="None"
        
        

        if newsoname:
            esong.song_title=newsoname
            db.session.commit()
        if newart:
            esong.song_artist=newart
            db.session.commit()

        
    solist=Song.query.all()
    return render_template("Editing.html",ename=ename,eart=eart,solist=solist,ustat=ustat,uid=uid)

  
    
    
