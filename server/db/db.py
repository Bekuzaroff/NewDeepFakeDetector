from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey

from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase): # basic declarative class for our database
    pass

db = SQLAlchemy(model_class=Base) # inherits from basic class

# Representations of all our db tables ----->
class User(db.Model):
    __tablename__ = "users" 
    user_id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    pswrd: Mapped[int] = mapped_column(nullable=False)
    create_date: Mapped[datetime] = mapped_column()

    def __repr__(self):
        return f"<User {self.username}>"

class Images(db.Model):
    __tablename__ = "images" 
    img_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    img_link: Mapped[str] = mapped_column(nullable=False)
    img_size: Mapped[int] = mapped_column(nullable=False)
    img_type: Mapped[str] = mapped_column(nullable=False)

    def __repr__(self):
        return f"<Image {self.img_link}>"