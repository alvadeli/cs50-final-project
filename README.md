# MusicDB
#### Video Demo:
#### Description:

A Flask web application that allows someone to keep track of and rate their favourite music albums.
The user can add new albums, edit existing albums and delete albums.

## templates

### layout.html
This file defines the basic layout of the website.
It contains a navbar for quick navigation through the site.
All other html files extend this file.

### index.html
The home page of this project.
Before displaying the file, the album data is read from the database.
The data is sent when the file is rendered. 
The album data is displayed in a table.

### enter_music_data.html
This is the first option for adding a new album.
To select this, the user must use the drop down menu in the navbar.
The html file is displayed in the input fields.
After pressing the Add button, the data is sent to the server.
The server validates the input and inserts the data into the music.db tables.
The user is redirected to the home page.

### edit_music_data.html

### search_musicbrainz_data

## py

### app.py

### models.py

This file contains sql alchemy model classes.
The sqlite3 tables of the music.db are mapped to these models.

tables/models:
* Album
* Artist
* Rating



### musicbrainz_functions.py
This file contains a function to fetch data from MusicBrainz with the Request HTTP Library
