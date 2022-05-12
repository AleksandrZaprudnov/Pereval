from sqlalchemy import Column, ForeignKey, Integer, Float, String
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    fam = Column(String)
    name = Column(String)
    otc = Column(String)
    phone = Column(String)

    pereval_add = relationship("PerevalAdded", back_populates="owner")


class Coords(Base):
    __tablename__ = 'coords'

    id = Column(Integer, primary_key=True, index=True)
    latitude = Column(Float)
    longitude = Column(Float)
    height = Column(Integer)

    owner_coords = relationship("PerevalAdded", back_populates="coords_add")


class PerevalAdded(Base):
    __tablename__ = 'pereval_added'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    coords_id = Column(Integer)
    status = Column(String)
    beautyTitle = Column(String)
    title = Column(String)
    other_titles = Column(String)
    connect = Column(String)
    winter = Column(String)
    summer = Column(String)
    autumn = Column(String)
    spring = Column(String)

    owner = relationship("User", back_populates="pereval_add")
    coords_add = relationship("Coords", back_populates="owner_coords")

