from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from database_declarative import Posts, Base
class postsDB:
	def __init__(self):
		self.engine = create_engine('sqlite:///colfax_likes.db')
		Base.metadata.bind = self.engine
		DBSession = sessionmaker(bind=self.engine)
		self.session = DBSession()
	def add(self, l):
		new_post = Posts(link=l, liked=1)
		self.session.add(new_post)
		self.session.commit()
		print("Added " + l + " to like database")
	def getLikes(self):
		for like in self.session.query(Posts):
			print(Posts.link)

db = postsDB()
#db.add("Tacos")
db.getLikes;