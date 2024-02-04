from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import DateTime, Integer, String
from datetime import datetime
from flask_migrate import Migrate

db = SQLAlchemy()

class Artist(db.Model):
    id: Mapped[int] = mapped_column(Integer(),primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

class Album(db.Model):
    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    release_date: Mapped[datetime] = mapped_column(DateTime(), nullable=False) 
    cover: Mapped[str] = mapped_column(String(255), nullable=True)
    artist_id: Mapped[int] = mapped_column(ForeignKey("artist.id"), nullable=False)

class Rating(db.Model):
    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    album_id: Mapped[int] = mapped_column(ForeignKey("album.id"), nullable=False)
    rating_value: Mapped[int] = mapped_column(Integer(), nullable=False)

