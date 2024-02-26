# MusicDB
#### Video Demo:
#### Description:

A Flask web application that allows someone to keep track of and rate their favourite music albums.
The user can add new albums, edit existing albums and delete albums. 
A sqlite database is used with SQLAlchemy. I used the orm function instead of raw sql.
This allows me to map the tables to python objects. Writing sql queries with SQLAlchemy is similar to writing raw sql queries.
This means that you do not have to learn a completely new syntax. 
For the design of the html elements I used bootstrap. This makes it easy to create simple but good looking pages without much effort.
To create dynamic content and display data structures in html I used jinja2.

The user has two options to add new albums. The first option is to enter all the necessary data manually.
The second option is to use the [MusicBrainz API](https://musicbrainz.org/doc/MusicBrainz_API). 
I used this option because it is free for non-commercial projects and no special account is required to retrieve the data.
You need to build search queries for the data you want. The results are returned in JSON format, which can then be processed on the server.

In order to structure and plan my project, I have created a Gantt chart using Latex.
The diagram can be found in the directory planning. I started with a research block for the technologies I wanted to use (SQL Alchemy and the MusicBrainsAPI).
After that I started to build a prototype. This part mainly consisted of creating the database tables and a simple html table to verify that the data retrieval worked.
With the prototype I started the implementation phase.
I used the prototype as a base and added all the features I wanted. 

# Files
Description of all files i created.

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
When the user enters the edit route by clicking the Edit button in the navbar
the album data table is displayed with an additional Actions column. The row contains two buttons, 'Edit' and 'Delete'.

### enter_music_data.html
This is the first option for adding a new album.
To select this, the user must use the drop down menu in the navigation bar.
The html file is displayed in the input fields.
When the Add button is pressed, the data is sent to the server.
The server validates the input and inserts the data into the music.db tables.
The user is redirected to the home page.

### edit_music_data.html
The file gets displayed after preesing the edit button of an album.
The user can update the album data here.

### search_musicbrainz_data.html
The user can enter an artist name and album name to search the [MusicBrainz API] (https://musicbrainz.org/doc/MusicBrainz_API).
The user can select an album from the search results and add it to the database. 
If the selected album has a cover art in the MusicBrainz database, the path will also be added to the database.

### enter_music_data.html
The second method of adding a new album is to enter the album details manually. 
With this method, the added album will have a default image as its cover.

## py

### app.py
Main file of the flask application. This file contains the flask application.
All possible routes are defined in this file. The main focus here is the interaction with the sqlite database.

Database operations are handled using sqlalchemy: 
* adding new music data to the database tables
* Deleting table rows 
* Update existing table rows 
* Reading route specific information and using the data with flask's render_template function.

All data that is required by a from or query for a route has the attribute "required" in the html files.
This is also checked on the server side in the routes.

### models.py

This file contains sql alchemy model classes.
The sqlite3 tables of music.db are mapped to these models.

Tables/models with columns:
* Album: id, title, release and artist_id (foreign key to artist.id). 
* Artist: id and name
* Rating: id, rating and album_id (foreign key to Album.id)
* MusicBrainzReleaseGroup: id, cover_url and album_id (foreign key to Album.id) 

### musicbrainz_functions.py
This file contains a function that interacts with the MusicBrainz API. 
To retrieve data from the MusicBrainz API, the Request HTTP library is used.
All functions use a try except block to catch errors if the request is invalid or the MusicBrainz API is not reachable.
