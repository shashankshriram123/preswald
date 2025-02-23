from sqlalchemy.orm import sessionmaker
from database_setup import engine, Player, Rating, ActivityLog
from datetime import datetime

Session = sessionmaker(bind=engine)
session = Session()

# Example Player Data
player = Player(
    player_id=11177810,
    username="fabianocaruana",
    name="Fabiano Caruana",
    title="GM",
    avatar="https://images.chesscomfiles.com/uploads/v1/user/11177810.9dfc8d31.200x200o.9a9eccebc07c.png",
    profile_url="https://www.chess.com/member/FabianoCaruana",
    country="US",
    followers=20395,
    last_online=datetime.fromtimestamp(1740163219),
    joined=datetime.fromtimestamp(1363533272),
    status="premium",
    is_streamer=False,
    verified=False,
    league="Champion"
)

session.add(player)
session.commit()

# Example Rating Data
rating = Rating(
    player_id=11177810,
    format="chess_rapid",
    last_rating=663,
    last_rating_date=datetime.fromtimestamp(1734149491),
    last_rating_rd=116,
    best_rating=699,
    best_rating_date=datetime.fromtimestamp(1733991217),
    best_game_link="https://www.chess.com/game/live/83096119541",
    wins=251,
    losses=211,
    draws=26
)

session.add(rating)
session.commit()

# Example Activity Log Data
activity = ActivityLog(
    player_id=11177810,
    date=datetime.strptime("2023-02-19", "%Y-%m-%d"),
    games_played=2,
    times_played_white=1,
    times_played_black=1,
    wins=0,
    checkmated=1,
    stalemates=0,
    resigned=1
)

session.add(activity)
session.commit()

session.close()
