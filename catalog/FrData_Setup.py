# starting code for furniture item catalog udacity project
import sys
import os
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine

''' This is my Item Ctalog project on Furniture items  '''
Base = declarative_base()


class FurnitureUser(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    email = Column(String(200), nullable=False)


class FrCompanyName(Base):
    __tablename__ = 'furniturecompanyname'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(FurnitureUser, backref="furniturecompanyname")

    @property
    def regular(self):
        """Return objects data in easily serializeable formats"""
        return {
            'name': self.name,
            'id': self.id
        }


class FurnitureName(Base):
    __tablename__ = 'furniturename'
    id = Column(Integer, primary_key=True)
    name = Column(String(350), nullable=False)
    description = Column(String(150))
    color = Column(String(150))
    price = Column(String(10))
    model = Column(String(250))
    date = Column(DateTime, nullable=False)
    furniturecompanynameid = Column(Integer, ForeignKey(
                                    'furniturecompanyname.id'))
    furniturecompanyname = relationship(
        FrCompanyName, backref=backref(
            'furniturename', cascade='all,delete'))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(FurnitureUser, backref="furniturename")

    @property
    def regular(self):
        """Return objects data in easily serializeable formats"""
        return {
            'name': self. name,
            'description': self. description,
            'color': self. color,
            'price': self. price,
            'model': self. model,
            'date': self. date,
            'id': self. id
        }

engine = create_engine('sqlite:///furniture.db')
print("Successfully created furniture database")
Base.metadata.create_all(engine)
