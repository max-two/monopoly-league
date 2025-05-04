from db import create_db_and_tables, get_session
from models import CoinFlip, CoinFlipBet, CoinFlipSide, League, NflTeam, Game, User


def did_coin_flip_win(bet: CoinFlipBet):
    return bet.side == bet.coin_flip.winning_side

def get_bet_multiplier(user: User):
    return 1.5 if user.league == League.LOWER else 1

def calc_bet_winnings(bet: CoinFlipBet):
    if did_coin_flip_win(bet):
        multiplier = get_bet_multiplier(bet.user)
        return bet.amount * multiplier
    else:
        return -bet.amount


if __name__ == "__main__":
    # Create db
    create_db_and_tables()

    # Get a session generator
    session_generator = get_session()
    
    # Get the actual session
    db = next(session_generator)

    try:
        # Create Users
        max = User(name="Max", league=League.LOWER)
        db.add(max)
        ben = User(name="Ben", league=League.UPPER) 
        db.add(ben)
        jesus = User(name="Jesus", league=League.LOWER)
        db.add(jesus)
        cale = User(name="Cale", league=League.LOWER)
        db.add(cale)
        asher = User(name="Asher", league=League.LOWER)
        db.add(asher)
        mikey = User(name="Mikey", league=League.LOWER)
        db.add(mikey)
        joey = User(name="Joey", league=League.UPPER)
        db.add(joey)
        aaron = User(name="Aaron", league=League.UPPER)
        db.add(aaron)
        mason = User(name="Mason", league=League.UPPER)
        db.add(mason)
        justin = User(name="Justin", league=League.UPPER)
        db.add(justin)

        # Create Games
        # Wild Card Round (Week 19)
        
        # Divisional Round (Week 20)

        # Conference Championships (Week 21)

        # Super Bowl (Week 22)
        super_bowl = Game(week=22, home_team=NflTeam.EAGLES, away_team=NflTeam.CHIEFS)
        db.add(super_bowl)

        # Create CoinFlips
        super_bowl_coin_flip = CoinFlip(game=super_bowl, winning_side=CoinFlipSide.TAILS)
        db.add(super_bowl_coin_flip)

        # Create CoinFlipBets
        db.add(CoinFlipBet(user=max, coin_flip=super_bowl_coin_flip, side=CoinFlipSide.TAILS, amount=20))
        db.add(CoinFlipBet(user=cale, coin_flip=super_bowl_coin_flip, side=CoinFlipSide.HEADS, amount=20))

        db.commit()

        # Calculate winnings per user
        for user in [max, cale]:
            winnings = 0
            for bet in user.coin_flip_bets:
                winnings += calc_bet_winnings(bet)

            print(f"{user.name} won {winnings} dollars")

    finally:
        # Make sure to close the session properly
        try:
            next(session_generator)  # This triggers the code after yield
        except StopIteration:
            pass
