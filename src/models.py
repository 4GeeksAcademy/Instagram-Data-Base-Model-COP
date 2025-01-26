import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Text, Table
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er
from datetime import datetime

Base = declarative_base()

# Many-to-Many relationship table for followers
followers = Table('followers',
    Base.metadata,
    Column('follower_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('followed_id', Integer, ForeignKey('user.id'), primary_key=True)
)

# Many-to-Many relationship table for post likes
post_likes = Table('post_likes',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('post_id', Integer, ForeignKey('post.id'), primary_key=True)
)

class User(Base):
    __tablename__ = 'user'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(250), nullable=False)
    full_name = Column(String(120), nullable=False)
    bio = Column(Text)
    profile_picture = Column(String(250))
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Integer, default=1)
    
    # Relationships
    posts = relationship('Post', back_populates='user')
    comments = relationship('Comment', back_populates='user')
    followers = relationship('User', 
        secondary=followers,
        primaryjoin=(followers.c.followed_id == id),
        secondaryjoin=(followers.c.follower_id == id),
        backref='following'
    )

class Post(Base):
    __tablename__ = 'post'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    image_url = Column(String(250), nullable=False)
    caption = Column(Text)
    location = Column(String(150))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship('User', back_populates='posts')
    comments = relationship('Comment', back_populates='post')
    likes = relationship('User', secondary=post_likes, backref='liked_posts')

class Comment(Base):
    __tablename__ = 'comment'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship('User', back_populates='comments')
    post = relationship('Post', back_populates='comments')

class Story(Base):
    __tablename__ = 'story'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    media_url = Column(String(250), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)
    
    # Relationships
    user = relationship('User')

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e