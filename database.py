from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine('postgresql://127.0.0.1:5432/mydb', echo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()


class place(Base):
    __tablename__ = 'place'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    phone = Column(String(11))
    address = Column(String)
    map = Column(String)
    panorama = Column(String)

    def __init__(self, id, name, phone, address, map, panorama):
        self.id = id
        self.name = name
        self.phone = phone
        self.address = address
        self.map = map
        self.panorama = panorama


Base.metadata.create_all(bind=engine)

session = Session()
"""
Radius3 = place('4', 'Radius3', '84951234565', 'Научный проезд 15', 'https://goo-gl.ru/4Sxt', 'https://goo-gl.ru/4Sxw')

session.add(Radius3)
session.commit()
"""
session.close()