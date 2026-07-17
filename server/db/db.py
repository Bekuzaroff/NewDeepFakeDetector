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
    pswrd: Mapped[str] = mapped_column(nullable=False)
    create_date: Mapped[datetime] = mapped_column()

    def __repr__(self):
        return f"<User {self.username}>"

class Profession(db.Model):
    __tablename__ = "professions" 
    profession_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    desc: Mapped[str] = mapped_column(nullable=False)
    def __repr__(self):
        return f"<Profession {self.profession_id}>"

class Topic(db.Model):
    __tablename__ = "topics" 
    topic_id: Mapped[int] = mapped_column(primary_key=True)
    prof_id: Mapped[int] = mapped_column(ForeignKey("professions.profession_id"))
    name: Mapped[str] = mapped_column(nullable=False)

    def __repr__(self):
        return f"<Topic {self.topic_id}>"

class Lesson(db.Model):
    __tablename__ = "lessons" 
    lesson_id: Mapped[int] = mapped_column(primary_key=True)
    topic_id: Mapped[int] = mapped_column(ForeignKey("topics.topic_id"))
    name: Mapped[str] = mapped_column(nullable=False)

    def __repr__(self):
        return f"<Lesson {self.lesson_id}>"

class Exercise(db.Model):
    __tablename__ = "exercises" 
    exercise_id: Mapped[int] = mapped_column(primary_key=True)
    lesson_id: Mapped[int] = mapped_column(ForeignKey("lessons.lesson_id"))
    name: Mapped[str] = mapped_column(nullable=False)

    def __repr__(self):
        return f"<Exercise {self.exercise_id}>"

class UsersProfessions(db.Model):
    __tablename__ = "users_professions" 
    profession_id: Mapped[int] = mapped_column(ForeignKey("professions.profession_id"), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), primary_key=True)
    def __repr__(self):
        return f"<Profession {self.profession_id} of User {self.user_id}>"

