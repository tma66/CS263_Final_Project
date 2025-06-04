from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    author = relationship("User", back_populates="posts")

User.posts = relationship("Post", order_by=Post.id, back_populates="author")

engine = create_engine('sqlite:///blog.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def search_users(username=None, email=None):
    query = session.query(User)
    if username:
        query = query.filter(User.username.like(f'%{username}%'))
    if email:
        query = query.filter(User.email.like(f'%{email}%'))
    return query.all()

def search_posts(title=None, content=None, author_id=None):
    query = session.query(Post)
    if title:
        query = query.filter(Post.title.like(f'%{title}%'))
    if content:
        query = query.filter(Post.content.like(f'%{content}%'))
    if author_id:
        query = query.filter(Post.user_id == author_id)
    return query.all()