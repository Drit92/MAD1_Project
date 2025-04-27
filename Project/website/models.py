from . import db




class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    user_name=db.Column(db.String(100),unique=True , nullable = False)
    user_password = db.Column(db.String(100))
    user_status = db.Column(db.String)
    revs = db.relationship("Review", backref = "user")
    user_playlists = db.relationship("Playlist", backref = "user")


class Song(db.Model):
    song_id = db.Column(db.Integer, primary_key=True)
    song_title= db.Column(db.String , nullable = False)
    song_artist = db.Column(db.String,db.ForeignKey("album.song_artist"))
    song_avg_review = db.Column(db.Float)
    s_revs= db.relationship("Review", backref = "song")
    song_path=db.Column(db.Text)
    song_del_path=db.Column(db.Text)
    song_datetime=db.Column(db.Text)
    song_lyrics=db.Column(db.String)
    total_point=db.Column(db.Integer)
    total_revs=db.Column(db.Integer)


    def __repr__(self):
        return f'<Song "{self.song_title}">'

association = db.Table('association',
                    db.Column('playlist_id', db.Integer, db.ForeignKey('playlist.playlist_id'),primary_key=True),
                    db.Column('song_id', db.Integer, db.ForeignKey('song.song_id'),primary_key=True)
                    )  
    

class Playlist(db.Model):
    playlist_id = db.Column(db.Integer, primary_key=True)
    playlist_name = db.Column(db.String)
    user_id = db.Column(db.Integer,db.ForeignKey("user.user_id"))
    members = db.relationship("Song", secondary = "association",backref = "playlist")

    def __repr__(self):
        return f'<Playlist "{self.playlist_name}">'


class Review(db.Model):
    review_id = db.Column(db.Integer,primary_key=True)
    song_id = db.Column(db.Integer,db.ForeignKey("song.song_id"))
    user_id = db.Column(db.Integer,db.ForeignKey("user.user_id"))
    review = db.Column(db.Integer)

class Album(db.Model):
    album_id = db.Column(db.Integer, primary_key=True)
    album_genere= db.Column(db.String)
    song_artist = db.Column(db.String)
    works = db.relationship("Song",backref = "album")