from sqlalchemy.orm import Session
from app.models.user import User
from app.models.game import Game

def get_games_by_user(db: Session, username: str):
    return (
        db.query(Game)
        .join(Game.user)  # only if using relationship
        .filter(User.username == username)
        .all()
    )


def add_game(db: Session, username: str, title: str, description: str | None):
    user_obj = db.query(User).filter(User.username == username).first()
    if not user_obj:
        raise ValueError("User not found")

    game = Game(user=user_obj, title=title, description=description)
    db.add(game)
    db.commit()
    db.refresh(game)
    return game

