import os

from flask import Flask, flash, jsonify, redirect, render_template, request, session, abort,send_from_directory
from flask_sqlalchemy import SQLAlchemy
import requests
import sqlalchemy as sqla
from datetime import datetime
from models import Artist, Album, Rating, MusicBrainzReleaseGroup ,db
from musicbrainz_functions import fetch_musicbrainz_data,get_album_cover_url
from werkzeug.utils import secure_filename

# Configure application
app = Flask(__name__)

# Configure database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///music.db" 
app.config['ALBUM_COVER_PATH'] = 'album_covers'
db.init_app(app)

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
def index(alert_message=""):
    select_album_data = sqla.select(Album,Artist,Rating,MusicBrainzReleaseGroup)\
        .join(Artist, Album.artist_id == Artist.id)\
        .join(Rating, Album.id == Rating.album_id, isouter=True)\
        .join(MusicBrainzReleaseGroup, MusicBrainzReleaseGroup.album_id == Album.id, isouter=True)
    
    album_data = db.session.execute(select_album_data).all()
    #alert_message = session.pop('alert_message', None) 

    return render_template("index.html", album_data=album_data, show_actions=False, alert_message=alert_message)

@app.route('/album_covers/<filename>')
def upload(filename):
    return send_from_directory(app.config['ALBUM_COVER_PATH'], filename)

@app.route("/enter_music_data", methods=["GET"])
def enter_music_data():
    return render_template("enter_music_data.html")


@app.route("/add_album", methods=["POST"])
def add_album():    
    # Get Data from Form
    artist_name = request.form.get("artist")
    album_title = request.form.get("title")
    release_date = request.form.get("release_date")
    rating_value = request.form.get("rating")
    mbrainz_release_group_id = request.form.get("mbrainz_release_group_id")

    if not artist_name or not album_title or not release_date:
        return abort(400, "Missing required fields")
    
    album_title = album_title.strip()
    artist_name = artist_name.strip()
    if release_date.count("-") == 2:
        release_date = datetime.strptime(release_date, "%Y-%m-%d").date()
    else:
        release_date = datetime.strptime(release_date, "%Y").date()

    # add artist
    select_artist = sqla.select(Artist).where(Artist.name == artist_name)
    artist = db.session.scalars(select_artist).first()
    
    if not artist:
        artist = Artist(name=artist_name)
        db.session.add(artist)
        db.session.commit()

    # add or update Album
    select_album = sqla.select(Album).where(Album.title == album_title).where(Album.artist_id == artist.id)           
    album = db.session.scalars(select_album).first()
    
    if album:
        alert_message = f"{album_title} from {artist_name} already exists!"
        return index(alert_message)
    else:
        album = Album(title = album_title, release_date = release_date, artist_id = artist.id)
        db.session.add(album)
    db.session.commit()
 
    # add rating for album
    if rating_value:
        try:
            rating_value = int(rating_value)
        except:
            return abort(400, f"rating_value {rating_value} could not be processed")    
        select_rating = sqla.select(Rating).where(Rating.album_id == album.id)
        rating = db.session.scalars(select_rating).first()
        if rating:
            rating.rating_value = rating_value
        else:
            new_rating = Rating(album_id=album.id, rating_value=rating_value)
            db.session.add(new_rating)
        db.session.commit()    

    if mbrainz_release_group_id:
        cover_url = get_album_cover_url(mbrainz_release_group_id)
        filename = None
        if cover_url:
             filename = f"{mbrainz_release_group_id}.jpg"
             save_image_from_url(cover_url, filename)
        new_release_group = MusicBrainzReleaseGroup(cover_url=cover_url, release_group_id=mbrainz_release_group_id, album_id=album.id, cover_filename=filename)
        db.session.add(new_release_group)
        db.session.commit()

    alert_message = f"Added {album_title} from {artist_name}!"
    return index(alert_message)
    

@app.route("/search_musicbrainz_data", methods=["POST", "GET"])
def search_musicbrainz_data():
    if request.method == "GET":
        return render_template("search_musicbrainz_data.html")
    
    artist = request.form.get("artist_search")
    album = request.form.get("album_search")

    if not artist or not album:
        return abort(400, "Missing required fields")
    
    query_params = {
        "release": album,
        "artist": artist     
    }

    release_groups = fetch_musicbrainz_data(query_params)

    if release_groups is not None:
        return render_template("search_musicbrainz_data.html", release_groups=release_groups, artist=artist, album=album, display_results=True)
    
    return abort({"error": "Failed to fetch data from MusicBrainz API."}), 500


@app.route("/edit_music_data", methods=["GET", "POST"])
def edit_music_data():
    if request.method == "GET":
        album_id = request.args.get("album_id")
        if not album_id:
            return abort(400, "album_id missing")
        try:
            album_id = int(album_id)
        except:
            return abort(400, f"album_id {album_id} could not be processed")    
        
        select_album_data = sqla.select(Album,Artist,Rating).filter(Album.id == album_id)\
            .join(Album, Album.artist_id == Artist.id)\
            .join(Rating, Album.id == Rating.album_id, isouter=True)
        
        album_data = db.session.execute(select_album_data).first()

        if not album_data:
            return redirect("/")

        return render_template("edit_music_data.html", album_data = album_data)
    
    ## POST 

    # Get input data
    album_id = request.form.get("album_id")
    artist_name = request.form.get("artist")
    album_title = request.form.get("album")
    release_date = request.form.get("release_date")
    rating_value = request.form.get("rating")

    if not album_id or not artist_name or not album_title or not release_date:
        return abort(400, "Missing required fields")
    
    album_title = album_title.strip()
    artist_name = artist_name.strip()
    release_date = datetime.strptime(release_date, "%Y-%m-%d").date()

    try:
        album_id = int(album_id)
    except:
        return abort(400, f"album_id {album_id} could not be processed")    

    select_album_data = sqla.select(Album,Artist,Rating)\
        .filter(Album.id == album_id)\
        .join(Album, Album.artist_id == Artist.id)\
        .join(Rating, Album.id == Rating.album_id, isouter=True)
    
    album_data = db.session.execute(select_album_data).first()

    if album_data is None:
        abort(400, f"Album with id {album_id} not found")

    album, artist, rating = album_data.t;   
    album.title = album_title
    album.release_date = release_date
    artist.name = artist_name

    if rating_value:
        try:
            rating_value = int(rating_value)
        except:
            return abort(400, f"rating_value {rating_value} could not be processed")    
        if rating:
            rating.rating_value = rating_value
        else:
            new_rating = Rating(album_id = album.id, rating_value = rating_value)
            db.session.add(new_rating)
    
    db.session.commit()
    return redirect("/edit")


@app.route("/delete", methods=["POST"])
def delete():
    album_id = request.form.get("album_id")

    if not album_id:
        return abort(400, "album_id not found")
    
    try:
        album_id = int(album_id)
    except:
        return abort(400, f"album_id {album_id} could not be processed")   

    delete_rating = sqla.delete(Rating).where(Rating.album_id == album_id)
    db.session.execute(delete_rating)
    
    get_cover_filepath = sqla.select(MusicBrainzReleaseGroup.cover_filename).where(MusicBrainzReleaseGroup.album_id == album_id)
    cover_filename = db.session.execute(get_cover_filepath).scalar_one_or_none()

    if cover_filename:
        album_cover_path = os.path.join(app.config['ALBUM_COVER_PATH'], cover_filename)
        os.remove(album_cover_path)
        
    delete_release_group = sqla.delete(MusicBrainzReleaseGroup).where(MusicBrainzReleaseGroup.album_id == album_id)
    db.session.execute(delete_release_group)

    delete_album = sqla.delete(Album).where(Album.id == album_id)
    db.session.execute(delete_album)

    db.session.commit()
    return redirect("/edit")

@app.route("/edit", methods=["GET"])
def edit():
    select_album_data = sqla.select(Album,Artist,Rating,MusicBrainzReleaseGroup)\
        .join(Artist, Album.artist_id == Artist.id)\
        .join(Rating, Album.id == Rating.album_id, isouter=True)\
        .join(MusicBrainzReleaseGroup, MusicBrainzReleaseGroup.album_id == Album.id, isouter=True)
    album_data = db.session.execute(select_album_data).all()

    return render_template("index.html", album_data=album_data, show_actions=True)


@app.route("/img_test", methods=["GET"])
def img_test():
    select_album_data = sqla.select(Album,Artist,Rating,MusicBrainzReleaseGroup)\
        .join(Artist, Album.artist_id == Artist.id)\
        .join(Rating, Album.id == Rating.album_id, isouter=True)\
        .join(MusicBrainzReleaseGroup, MusicBrainzReleaseGroup.id == Album.id, isouter=True)
    album_data = db.session.execute(select_album_data).all()

    return render_template("img_test.html", album_data=album_data, show_actions=False)

def save_image_from_url(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(os.path.join(app.config['ALBUM_COVER_PATH'], filename), 'wb') as f:
            f.write(response.content)