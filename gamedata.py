# importing modules for creating database
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from database_setup import Category, Base, CategoryItem, User

engine = create_engine('sqlite:///gamedb.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = scoped_session(sessionmaker(bind=engine))
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Dummy user
User1 = User(name="sonu", email="vermasonu791@gmail.com")

# Indorgames
category1 = Category(name="Indor game")

session.add(category1)
session.commit()

# types of indore games
item1 = CategoryItem(name="Sorting", description="For younger kids, sorting " +
                                                 "colors is the easiest to" +
                                                 "start.More advanced" +
                                                 "can be had by the texture" +
                                                 "a surface or type of" +
                                                 "object", category=category1)

session.add(item1)
session.commit()

item2 = CategoryItem(name="Hide and Seek", description="This has to be one of" +
                                                       "oldest games on planet" +
                                                       "!", category=category1)

session.add(item2)
session.commit()

item3 = CategoryItem(name="Rock Paper and Scissor", description="This has to be" +
                                                                "one of" +
                                                                "oldest games on" +
                                                                "planet Earth"
                                                                , category=category1)

session.add(item3)
session.commit()

item4 = CategoryItem(name="Marbles", description="Intresting game", category=category1)

session.add(item4)
session.commit()

# outdorgames
category1 = Category(name="outdor game")

session.add(category1)
session.commit()

# types of outdorgames
item1 = CategoryItem(name="Frozen T-Shirt Race", description="Soak a bunch" +
                                                             "of t-shirts in water" +
                                                             ", place them in" +
                                                             "plastic bags," +
                                                             "and then stick them" +
                                                             "in the freezer" +
                                                             , category=category1)

session.add(item1)
session.commit()

item2 = CategoryItem(name="slid and toss", description="Slip" +
                     "and slides are fun enough on their own,"+
                     "but turning one into a game? Even better. ", category=category1)

session.add(item2)
session.commit()

item3 = CategoryItem(name="Flipper Fill Up", description="A relay" +
                     "race involving silly flippers and a very, very full bucket of water.", category=category1)

session.add(item3)
session.commit()


# videogames
category1 = Category(name="video game")

session.add(category1)
session.commit()

# types of videogames
item1 = CategoryItem(name="Angry Birds", description="awesome" +
                     "game every one play this game", category=category1)

session.add(item1)
session.commit()

item2 = CategoryItem(name="Gran tourismo", description="Racing game", category=category1)

session.add(item2)
session.commit()

item3 = CategoryItem(name="Mario", description="The player" +
                     "gains points by defeating multiple enemies" +
                     "consecutively and can participate in a bonus" +
                     "round to gain more points. ", category=category1)

session.add(item3)
session.commit()

item4 = CategoryItem(name="Super Smash Bros.", description="Since" +
                     "the original launched on the Nintendo 64 in 1999," +
                     "the Super Smash Bros. games have become no-brainers for Nintendo fans", category=category1)

session.add(item4)
session.commit()

# sports
category1 = Category(name="sports")

session.add(category1)
session.commit()

# types of sports
item1 = CategoryItem(name="Hockey", description="Hockey is" +
                     "a sport in which two teams play against each other by trying to" +
                     "maneuver a ball or a puck into the opponent's goal using a hockey stick", category=category1)

session.add(item1)
session.commit()

item2 = CategoryItem(name="Football", description="Two teams of usually between"+
                     "11 and 18 players; some variations that have fewer" +
                     "players (five or more per team) are also popular.", category=category1)

session.add(item2)
session.commit()

item3 = CategoryItem(name="Cricket", description="Cricket is a" +
                     "national sport which is played between two teams of" +
                     "eleven players each who score runs (points)", category=category1)

session.add(item3)
session.commit()


# lan game
category1 = Category(name="Lan Gaming")

session.add(category1)
session.commit()

# type of lan game
item1 = CategoryItem(name="CS GO", description="Counter-Strike: Global" +
                     "Offensive (CS:GO) is a first-person shooter video" +
                     "game which is a part of the Counter-Strike series", category=category1)

session.add(item1)
session.commit()

item2 = CategoryItem(name="Dota2", description="Dota 2 is a multiplayer online battle arena (MOBA)", category=category1)

session.add(item2)
session.commit()

item2 = CategoryItem(name="Far-cry", description="Far Cry is a" +
                     "first-person shooter video game developed by Crytek Studios from Germany", category=category1)

session.add(item2)
session.commit()

print('items added')
