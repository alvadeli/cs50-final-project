from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import Integer, String,Date
from datetime import date

db = SQLAlchemy()

class Artist(db.Model):
    id: Mapped[int] = mapped_column(Integer(),primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

class Album(db.Model):
    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    release_date: Mapped[date] = mapped_column(Date(), nullable=False) 
    cover: Mapped[str] = mapped_column(String(255), nullable=True)
    artist_id: Mapped[int] = mapped_column(ForeignKey("artist.id"), nullable=False)

class Rating(db.Model):
    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    album_id: Mapped[int] = mapped_column(ForeignKey("album.id"), nullable=False, unique=True)
    rating_value: Mapped[int] = mapped_column(Integer(), nullable=False)

class MusicBrainzReleaseGroup(db.Model):
    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    cover_url: Mapped[str] = mapped_column(String(255), nullable=True)
    release_group_id: Mapped[str] = mapped_column(String(100))
    album_id: Mapped[int] = mapped_column(ForeignKey("album.id"), nullable=False, unique=True)
    

