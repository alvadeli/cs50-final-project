import os

from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
#from flask_migrate import Migrate
from datetime import datetime
from models import Artist, Album, Rating, db

# Configure application
app = Flask(__name__)

# Configure database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///music.db" 
#db = SQLAlchemy(app)
db.init_app(app)
# migrate = Migrate(app, db)


with app.app_context():    
    db.create_all()

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["POST", "GET"])
def index():
    select_album_data = select(Album,Artist,Rating).join(Artist, Album.artist_id == Artist.id).join(Rating, Album.id == Rating.album_id, isouter=True)
    album_data = db.session.execute(select_album_data).all()

    # for album,artist,rating in album_data:
    #     rating_value = rating.rating_value if rating else ""
    #     print(f"{album.id} {album.title} {artist.name} {rating_value}")

    return render_template("index.html", album_data=album_data)


@app.route("/enter_music_data", methods=["POST", "GET"])
def enter_music_data():
    if request.method == "GET":
        return render_template("enter_music_data.html")
    
    artist_name = request.form.get("artist")
    album_title = request.form.get("album")
    release_date = request.form.get("release_date")
    rating_value = request.form.get("rating")

    # if not artist or album or release_date:
    #     # TODO Error Handling
    #     render_template("enter_music_data.html")

    release_date = datetime.strptime(release_date, "%Y-%m-%d").date()
    select_artist = select(Artist).where(Artist.name == artist_name)
    artist = db.session.scalars(select_artist).first()
    
    if not artist:
        artist = Artist(name=artist_name)
        db.session.add(artist)
        db.session.commit()
               
    select_album = select(Album).where(Album.title == album_title).where(Album.artist_id == artist.id)           
    album = db.session.scalars(select_album).first()
    
    if album:
        album.release_date = release_date
    else:
        album = Album(title = album_title, release_date = release_date, artist_id = artist.id)
        db.session.add(album)
    db.session.commit()
 
    if rating_value:
        select_rating = select(Rating).where(Rating.album_id == album.id)
        rating = db.session.scalars(select_rating).first()
        if rating:
            rating.rating_value = rating_value
        else:
            new_rating = Rating(album_id = album.id, rating_value = rating_value)
            db.session.add(new_rating)
        db.session.commit()    

    return redirect("/")
    
@app.route("/edit_music_data", methods=["GET", "POST"])
def edit_music_data():
    if request.method == "GET":
        album_id = request.args.get("album_id")
        if not album_id:
            redirect("/")
        try:
            album_id = int(album_id)
        except:
            return redirect("/")    
        
        select_album_data = select(Album,Artist,Rating).filter(Album.id == album_id).join(Album, Album.artist_id == Artist.id).join(Rating, Album.id == Rating.album_id, isouter=True)
        album_data = db.session.execute(select_album_data).first()

        if not album_data:
            return redirect("/")

        return render_template("edit_music_data.html", album_data = album_data)
    
    #TODO Update Album data,

    #Delecte Add new Artist if neccessary and delete artist with no refs

    return redirect("/")
