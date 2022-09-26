from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import random
import string
db=SQLAlchemy()

class User(db.Model):
	id=db.Column(db.Integer(),primary_key=True)
	username=db.Column(db.String(80))
	email=db.Column(db.String(80))
	password=db.Column(db.Text())
	created_at=db.Column(db.DateTime(),default=datetime.now())
	updated_at=db.Column(db.DateTime(),onupdate=datetime.now())


	def __repr__(self):
		return self.username

class Bookmark(db.Model):
	id=db.Column(db.Integer(),primary_key=True)
	body=db.Column(db.Text(),nullable=True)
	url=db.Column(db.Text(),nullable=False)
	short_url=db.Column(db.String(3),nullable=True)
	visits=db.Column(db.Integer(),default=0)
	user_id=db.Column(db.Integer(),db.ForeignKey('user.id'))
	created_at=db.Column(db.DateTime(),default=datetime.now())
	updated_at=db.Column(db.DateTime(),onupdate=datetime.now())

	def generate_short_characaters(self):
		characters=string.digit+string.asciii_letters
		picked_characters=''.join(random.choices(characters,k=3))
		link=self.query.filter_by(short_url=picked_characters).first()
		if link:
			self.generate_short_characters()
		else:
			return picked_characters

	def __init__(self,**kwargs):
		super().__init__(self,**kwargs)
		self.short_url=self.generate_short_characters()

	def __repr__(self) ->str:
		return 'Bookmark>>> {self.url}'	

