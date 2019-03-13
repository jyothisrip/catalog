from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime
from FrData_Setup import *

# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

dbSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = dbSession()

# Delete FrCompanyName if exisitng.
session.query(FrCompanyName).delete()
# Delete FurnitureName if exisitng.
session.query(FurnitureName).delete()
# Delete User if exisitng.
session.query(FurnitureUser).delete()

engine = create_engine('sqlite:///furniture.db')

# Create sample users data
mainuser1 = FurnitureUser(
    name="Polisetty Jyothi Sri", email="jyothisri0303@gmail.com")
session.add(mainuser1)
session.commit()
print ("Successfully Added First Furniture User")
# Create sample furniture companys
furcompany1 = FrCompanyName(
    name=" Nilkamal Ltd", user_id=1)
session.add(furcompany1)
session.commit()

furcompany2 = FrCompanyName(
    name="Wipro Furniture", user_id=1)
session.add(furcompany2)
session.commit

furcompany3 = FrCompanyName(
    name="Hulsta", user_id=1)
session.add(furcompany3)
session.commit()

furcompany4 = FrCompanyName(
    name="IKEA", user_id=1)
session.add(furcompany4)
session.commit()

furcompany5 = FrCompanyName(
    name="Godrej Interio", user_id=1)
session.add(furcompany5)
session.commit()


# Populare a furnitures with models for testing
# Using different users for furnitures names model also
furname1 = FurnitureName(name="Dining Sets",
                         description="Dining Sets",
                         color="black",
                         price="40,650Rs",
                         model="Stark Dining Chair",
                         date=datetime.datetime.now(),
                         furniturecompanynameid=1,
                         user_id=1)
session.add(furname1)
session.commit()

furname2 = FurnitureName(name="Home Furniture",
                         description="Home Utility Furniture",
                         color="black",
                         price="40,650Rs",
                         model="Computer Tables",
                         date=datetime.datetime.now(),
                         furniturecompanynameid=2,
                         user_id=1)
session.add(furname2)
session.commit()

furname3 = FurnitureName(name="Book Cases",
                         description="Book Cases",
                         color="White",
                         price="25,000Rs",
                         model="Book Cases",
                         date=datetime.datetime.now(),
                         furniturecompanynameid=3,
                         user_id=1)
session.add(furname3)
session.commit()

furname4 = FurnitureName(name="Cabinets",
                         description="Cabinets",
                         color="Black",
                         price="35,650Rs",
                         model="Cabinets",
                         date=datetime.datetime.now(),
                         furniturecompanynameid=4,
                         user_id=1)
session.add(furname4)
session.commit()

furname5 = FurnitureName(name="Console Tables",
                         description="Console Tables",
                         color="White",
                         price="28,650Rs",
                         model="Console Tables",
                         date=datetime.datetime.now(),
                         furniturecompanynameid=5,
                         user_id=1)
session.add(furname5)
session.commit()

furname6 = FurnitureName(name="Storage Cabinets",
                         description="Storage Cabinets",
                         color="Black",
                         price="24,000Rs",
                         model="Storage Cabinets",
                         date=datetime.datetime.now(),
                         furniturecompanynameid=5,
                         user_id=1)
session.add(furname6)
session.commit()


furname7 = FurnitureName(name="Entertainment Setters",
                         description="Entertainment Setters",
                         color="Silver",
                         price="49,000Rs",
                         model="Entertainment Setters",
                         date=datetime.datetime.now(),
                         furniturecompanynameid=3,
                         user_id=1)
session.add(furname7)
session.commit()

furname8 = FurnitureName(name="Side Boards",
                         description="Side Boards",
                         color="Black",
                         price="43,000Rs",
                         model="Side Boards",
                         date=datetime.datetime.now(),
                         furniturecompanynameid=4,
                         user_id=1)
session.add(furname8)
session.commit()

furname9 = FurnitureName(name="Sleepers",
                         description="Sleepers",
                         color="White",
                         price="34,000Rs",
                         model="Pull-Out Sofabeds",
                         date=datetime.datetime.now(),
                         furniturecompanynameid=2,
                         user_id=1)
session.add(furname9)
session.commit()

furname10 = FurnitureName(name="Sofas",
                          description="Sofas",
                          color="Black",
                          price="30,000Rs",
                          model="Three Seated Sofas",
                          date=datetime.datetime.now(),
                          furniturecompanynameid=1,
                          user_id=1)
session.add(furname10)
session.commit()
print("Your furniture details has been inserted in your database!")
