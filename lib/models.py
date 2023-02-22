#!/usr/bin/env python3

from sqlalchemy import (Column, String, Integer, ForeignKey)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


Base = declarative_base()

engine = create_engine('sqlite:///freebies.db')
Session = sessionmaker(bind=engine)
session = Session()

class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    founding_year = Column(Integer())

    freebies = relationship('Freebie', backref='company')
    devs = association_proxy('freebies', 'dev',
        creator=lambda dv: Freebie(dev=dv))

    def __repr__(self):
        return f'<Company {self.name}, {self.founding_year}>'

    def give_freebie(self, dev, item_name, value):
        new_freebie = Freebie(
            item_name = item_name,
            value = value,
            company_id = self.id,
            dev_id = dev.id
            )
        session.add(new_freebie)
        session.commit()
        return new_freebie

    @classmethod
    def oldest_company(cls):
        oldest_company = session.query(cls).order_by('founding_year')[0]
        return oldest_company


class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer(), primary_key=True)
    name= Column(String())

    freebies = relationship('Freebie', backref='dev')
    companies = association_proxy('freebies', 'company',
        creator=lambda cm: Freebie(company=cm))

    def __repr__(self):
        return f'<Dev {self.name}>'
    
    def recieved_one(self, item_name):
       for freebie in self.freebies:
        if item_name == freebie.item_name:
            return True
        else:
            return False
    
    def give_away(self, dev, freebie):
        if freebie in self.freebies:
            session.query(Freebie).filter(Freebie.id == freebie.id).update(
                {Freebie.dev_id: dev.id})
            session.commit()
        

class Freebie(Base):
    __tablename__ = 'freebies'

    id = Column(Integer(), primary_key=True)
    item_name = Column(String())
    value = Column(Integer())

    company_id = Column(Integer(), ForeignKey('companies.id'))
    dev_id = Column(Integer(), ForeignKey('devs.id'))


    def __repr__(self):
        return f'<Freebie {self.item_name} {self.value}>'

    def print_details(self):
       return f'{self.dev.name} owns a {self.item_name} from {self.company.name}.'


