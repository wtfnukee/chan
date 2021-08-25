from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import String, create_engine, select, Text
from sqlalchemy.dialects.postgresql import VARCHAR, JSONB

from app import app

db = SQLAlchemy(app)
migrate = Migrate(app, db)
engine = create_engine(url=app.config['SQLALCHEMY_DATABASE_URI'], echo=True)
connection = engine.connect()


class Board(db.Model):
    id = db.Column(VARCHAR(5), primary_key=True, unique=True, nullable=False)
    boardname = db.Column(Text(), unique=True, nullable=False)
    flags = db.Column(JSONB(120), nullable=False)
    restrictions = db.Column(JSONB(120), nullable=False)

    def __str__(self):
        return self.boardname

    def __repr__(self):
        return '<Board %r>' % self.boardname

    def get_boards(self):
        s = select('boards')
        return connection.execute(s)


b = Board()
print(b.get_boards())
