from sqlalchemy.orm import sessionmaker
from database_setup import engine, Player, Rating

Session = sessionmaker(bind=engine)
session = Session()

# Get player data
player = session.query(Player).filter_by(username="fabianocaruana").first()
print(f"Player: {player.name}, Title: {player.title}, Followers: {player.followers}")

# Get ratings
ratings = session.query(Rating).filter_by(player_id=11177810).all()
for rating in ratings:
    print(f"Format: {rating.format}, Last Rating: {rating.last_rating}")

session.close()
