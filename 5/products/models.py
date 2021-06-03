from sqlalchemy import create_engine, Column, Table, ForeignKey, MetaData
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Integer, String, Date, DateTime, Float, Boolean, Text)
from scrapy.utils.project import get_project_settings

Base = declarative_base()


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(get_project_settings().get("CONNECTION_STRING"))


def create_table(engine):
    Base.metadata.create_all(engine)


# Association Table for Many-to-Many relationship between Product and Subcategory
# https://docs.sqlalchemy.org/en/13/orm/basic_relationships.html#many-to-many
# product_subcategory = Table('product_subcategory', Base.metadata,
#     Column('product_id', Integer, ForeignKey('product.id')),
#     Column('subcategory_id', Integer, ForeignKey('subcategory.id'))
# )

class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True)
    name = Column('name', String(100), unique=True)
    subcategories = relationship('Subcategory', backref='category')  # One subcategory to many Quotes


class Subcategory(Base):
    __tablename__ = "subcategory"

    id = Column(Integer, primary_key=True)
    name = Column('name', String(100), unique=True)
    category_id = Column(Integer, ForeignKey('category.id'))  # Many subcategories to one category
    products = relationship('Product', backref='subcategory')  # One subcategory to many Quotes

    # Many to many example
    # products = relationship('Product', secondary='product_subcategory',
    #     lazy='dynamic', backref="subcategory")  # M-to-M for quote and tag


class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True)
    name = Column('name', String(100), unique=True)
    rate = Column('rate', Float)
    safety = Column('safety', Float)
    quality = Column('quality', Float)
    source = Column('source', String(100))
    subategory_id = Column(Integer, ForeignKey('subcategory.id'))  # Many products to one subcategory
