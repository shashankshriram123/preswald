from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, Date, TIMESTAMP, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

# PostgreSQL connection URL (replace with your credentials)
DATABASE_URL = "postgresql://chess_user:10047642@localhost/chess_db"

engine = create_engine(DATABASE_URL, echo=True)
Base = declarative_base()

# Player Table
class Player(Base):
    __tablename__ = 'players'

    player_id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    name = Column(String)
    title = Column(String)
    avatar = Column(String)
    profile_url = Column(String)
    country = Column(String)
    followers = Column(Integer)
    last_online = Column(TIMESTAMP)
    joined = Column(TIMESTAMP)
    status = Column(String)
    is_streamer = Column(Boolean)
    verified = Column(Boolean)
    league = Column(String)

    ratings = relationship("Rating", back_populates="player")
    tactics = relationship("Tactics", uselist=False, back_populates="player")
    puzzle_rush = relationship("PuzzleRush", uselist=False, back_populates="player")
    activity_logs = relationship("ActivityLog", back_populates="player")

# Ratings Table
class Rating(Base):
    __tablename__ = 'ratings'

    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey('players.player_id'))
    format = Column(String)
    last_rating = Column(Integer)
    last_rating_date = Column(TIMESTAMP)
    last_rating_rd = Column(Integer)
    best_rating = Column(Integer)
    best_rating_date = Column(TIMESTAMP)
    best_game_link = Column(String)
    wins = Column(Integer)
    losses = Column(Integer)
    draws = Column(Integer)

    player = relationship("Player", back_populates="ratings")

# Tactics Table
class Tactics(Base):
    __tablename__ = 'tactics'

    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey('players.player_id'))
    highest_rating = Column(Integer)
    highest_rating_date = Column(TIMESTAMP)
    lowest_rating = Column(Integer)
    lowest_rating_date = Column(TIMESTAMP)

    player = relationship("Player", back_populates="tactics")

# Puzzle Rush Table
class PuzzleRush(Base):
    __tablename__ = 'puzzle_rush'

    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey('players.player_id'))
    total_attempts = Column(Integer)
    score = Column(Integer)

    player = relationship("Player", back_populates="puzzle_rush")

# Activity Logs Table
class ActivityLog(Base):
    __tablename__ = 'activity_logs'

    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey('players.player_id'))
    date = Column(Date)
    games_played = Column(Integer)
    times_played_white = Column(Integer)
    times_played_black = Column(Integer)
    wins = Column(Integer)
    checkmated = Column(Integer)
    stalemates = Column(Integer)
    resigned = Column(Integer)

    player = relationship("Player", back_populates="activity_logs")

# Create all tables
Base.metadata.create_all(engine)
