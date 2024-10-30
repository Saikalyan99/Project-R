# import warnings
import sys
# import numpy as np
# with warnings.catch_warnings():
#     warnings.simplefilter("ignore")
# import pandas as pd

import sqlalchemy as al
from sqlalchemy import Table, Column, Integer, String, Float, Numeric
from sqlalchemy import ForeignKey, PrimaryKeyConstraint
from sqlalchemy import insert, select, update, delete, create_engine, text
from sqlalchemy.orm import Session, Mapped, DeclarativeBase
from sqlalchemy.orm import mapped_column, relationship

def print_ver():
    print(f'Python Version: {sys.version}')
    print(f'SQLAlchemy Version: {al.__version__}')
    # print(f'Numpy Version: {np.__version__}')
    # print(f'Pandas Version: {pd.__version__}')


class Base(DeclarativeBase):
    pass

class Stores(Base):
    __tablename__ = "stores"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    rating: Mapped[float] = mapped_column(Numeric(2,1), nullable=True)
    numrating: Mapped[int] = mapped_column(Integer, nullable=True)

    streetnum: Mapped[str] = mapped_column(String(50), nullable=False)
    streetname: Mapped[str] = mapped_column(String(50), nullable=False)
    aptnum: Mapped[str] = mapped_column(String(50), nullable=True)
    city: Mapped[str] = mapped_column(String(200), nullable=False)
    state: Mapped[str] = mapped_column(String(15), nullable=False)
    zip: Mapped[int] = mapped_column(Integer, nullable=False)
    country: Mapped[str] = mapped_column(String(20), nullable=False)
    pluscode: Mapped[str] = mapped_column(String(20), nullable=True)
    
    # Relationship to store_tags
    tags = relationship("StoreTags", back_populates="store")

    def __repr__(self) -> str:
        return f"""Stores(id={self.id!r}, 
        name={self.name!r}, 
        rating={self.rating!r}, 
        numrating={self.numrating!r}, 
        streetnum={self.streetnum!r}, 
        streetname={self.streetname!r}, 
        aptnum={self.aptnum!r}, 
        city={self.city!r}, 
        state={self.state!r}, 
        zip={self.zip!r}, 
        country={self.country!r}, 
        pluscode={self.pluscode!r})"""
    
class Tags(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(20), nullable=False)

    # Relationship to store_tags
    stores = relationship("StoreTags", back_populates="tag")

    def __repr__(self) -> str:
        return f"Tags(id={self.id!r}, name={self.name!r})"

class StoreTags(Base):
    __tablename__ = "store_tags"
    __table_args__ = (PrimaryKeyConstraint('storeid', 'tagid'),)

    storeid = mapped_column(ForeignKey("stores.id"))
    tagid = mapped_column(ForeignKey("tags.id"))

    # Relationships for bidirectional access
    store = relationship("Stores", back_populates="tags")
    tag = relationship("Tags", back_populates="stores")

    def __repr__(self) -> str:
        return f"StoreTags(storeid={self.storeid!r}, tagid={self.tagid!r})"

def main():
    # Store username and password as environment variables or in a config file
    username = "root"
    password = "Pr0jectR"
    host = "localhost"
    port = "3306"  # Default MySQL port
    database = "ProjectR"

    engine = create_engine(f"mysql+mysqlconnector://{username}:{password}@{host}:{port}", echo=True)
    with engine.connect() as conn:
        conn.execute(text(f"DROP DATABASE IF EXISTS {database}"))
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {database}"))

    engine = create_engine(f"mysql+mysqlconnector://{username}:{password}@{host}:{port}/{database}", echo=True)
    Base.metadata.create_all(engine)

if __name__ == '__main__':
    print_ver()
    main()
