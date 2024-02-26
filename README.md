# MusicDB
#### Video Demo:
#### Description:

A Flask web application that allows someone to keep track of and rate their favourite music albums.
The user can add new albums, edit existing albums and delete albums. 
A sqlite database is used with SQLAlchemy. I have this the orm function instead of raw sql.
With this i can mapped the tables to python objects. Creating sql queries with SQLAlchemy resembles writing raw sql queries.
This means you do not have to learn a completly new syntax. For the design of the html elements i have used bootstrap and jinja2 to create dynamic content.

The user has two options to add new albums. The first option is to enter all the required data manually.
The second option is to use the [MusicBrainz API](https://musicbrainz.org/doc/MusicBrainz_API). 
I have used this option because it is free for non-commercial projects and a special account is not required to fetch data.
You need to build search queries for the data you and want. The results are returned in JSON format can than be processed on the server.

## templates

### layout.html
This file defines the basic layout of the website.
It contains a navbar for quick navigation through the site.
All other html files extend this file.

### index.html
The home page of this project.
Before displaying the file, the album data is read from the database.
The data is sent when the file is rendered. 
The album data is displayed in a table with a default cover or the album cover if available.
If the user goes to the edit route by pressing the edit button in the navbar
the album data table gets displayed with an addtional column actions. The row contains of two buttons "edit" and "delete".

### enter_music_data.html
This is the first option for adding a new album.
To select this, the user must use the drop down menu in the navbar.
The html file is displayed in the input fields.
After pressing the Add button, the data is sent to the server.
The server validates the input and inserts the data into the music.db tables.
The user is redirected to the home page.

### edit_music_data.html
The file gets displayed after preesing the edit button of an album.
The user can update the album data here.

### search_musicbrainz_data.html
The user can input an artist name and an album name to search the [MusicBrainz API](https://musicbrainz.org/doc/MusicBrainz_API).
The user can select an ablum from the search results and add it to the database. 
If the selected album has a cover art in the musicbrainz database, the path gets added to the database as well.

### enter_music_data
The second method to add a new album, is to enter the album data manually. 
In this method the added album have an default image as cover.

## py

### app.py
main file of the flask app. This file contains the flask app.
All possible routes are defined in this file. The main focus here the interaction with the sqlite database.
The database operations are handled with sqlalchemy. 
The main operations are: 
* adding new music data to the the database tables
* deleting table rows 
* updating existing tables rows 
* reading route specific information and using the data with the render_template function of flask.

### models.py

This file contains sql alchemy model classes.
The sqlite3 tables of the music.db are mapped to these models.

tables/models with columns:
* Album: id ,title, release and artist_id (foreign key to Artist.id). 
* Artist: id and name
* Rating: id, rating and album_id (foreign key to Album.id)
* MusicBrainzReleaseGroup: id, cover_url and album_id (foreign key to Album.id) 

### musicbrainz_functions.py
This file contains a function which interact with the musicbrainz API. 
To fetch data from MusicBrainz API the Request HTTP Library is used.
All functions use a try except block, to catch errors if the request is invalid or the MusicBrains API is not reachable.
