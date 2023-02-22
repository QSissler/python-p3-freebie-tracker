#!/usr/bin/env python3
from faker import Faker
import random
from random import choice as rc
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///freebies.db')
Session = sessionmaker(bind=engine)
session = Session()

# Script goes here!
fake = Faker()
print("Seeding companies...")
from models import Company

def create_companies(): 
    companies = [
        Company(
            name=fake.company(),
            founding_year=random.randint(1950, 2022)
        )
        for i in range(50)]
    session.add_all(companies)
    session.commit()
    return companies

print("Seeding companies...")
from models import Dev

def create_devs():
    devs = [
         Dev(
         name=fake.company(),
    )
        for i in range(50)]
    session.add_all(devs)
    session.commit()
    return devs

print("Seeding freebies...")
from models import Freebie

def create_freebies():
    freebies = [
       Freebie(
            item_name=fake.name(),
            value=random.randint(1, 10)
    )
        for i in range(100)]
    session.add_all(freebies)
    session.commit()
    return freebies

def delete_records():
    session.query(Company).delete()
    session.query(Dev).delete()
    session.query(Freebie).delete()
    session.commit()

def relate_one_to_many(companies, devs, freebies):
    for freebie in freebies:
        freebie.company = rc(companies)
        freebie.dev = rc(devs)

    session.add_all(freebies)
    session.commit()
    return companies, devs, freebies

if __name__ == '__main__':
    delete_records()
    companies = create_companies()
    devs = create_devs()
    freebies = create_freebies()
    relate_one_to_many(companies, devs, freebies)

