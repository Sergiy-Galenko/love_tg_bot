from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, BigInteger
from sqlalchemy.orm import relationship
from .database import Base

class UserProfile(Base):
    __tablename__ = 'user_profiles'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(BigInteger, unique=True, index=True)  # Замість Integer використайте BigInteger
    username = Column(String, nullable=True)
    name = Column(String)
    age = Column(Integer)
    city = Column(String)
    gender = Column(String)
    hobby = Column(String, nullable=True)
    search_preference = Column(String)
    photo = Column(String, nullable=True)
    is_adult = Column(Boolean, default=False)
    premium_status = Column(Boolean, default=False)
    premium_duration = Column(String, nullable=True)
    min_age = Column(Integer, nullable=True)
    max_age = Column(Integer, nullable=True)

    likes_received = relationship("Like", foreign_keys='Like.target_user_id', back_populates="target")
    likes_given = relationship("Like", foreign_keys='Like.user_id', back_populates="user")

class Like(Base):
    __tablename__ = 'likes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user_profiles.user_id'))
    target_user_id = Column(Integer, ForeignKey('user_profiles.user_id'))

    user = relationship("UserProfile", foreign_keys=[user_id], back_populates="likes_given")
    target = relationship("UserProfile", foreign_keys=[target_user_id], back_populates="likes_received")
