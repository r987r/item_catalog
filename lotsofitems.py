from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData

from entries import Base, Category, Item

engine = create_engine('sqlite:///itemcatalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Clear all previous entries
for table in reversed(Base.metadata.sorted_tables):
	session.execute(table.delete())
	print "hello"
	session.commit()

#Add Categories
category = Category(name="Soccer")

session.add(category)
session.commit()

item0 = Item(name="Soccer ball", description="basic soccer ball",
                     category=category)
session.add(item0)
session.commit()

item1 = Item(name="Cleats", description="cleatzzz",
                     category=category)
session.add(item1)
session.commit()

category1 = Category(name="Baseball")

session.add(category1)
session.commit()

item2 = Item(name="baseball", description="basic base ball",
                     category=category1)
session.add(item2)
session.commit()

item3 = Item(name="Cleats", description="cleatzzz",
                     category=category1)
session.add(item3)
session.commit()
