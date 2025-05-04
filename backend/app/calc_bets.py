from typing import Callable
from db import create_db_and_tables, get_session
from models import CoinFlip, CoinFlipBet, CoinFlipSide, League, NflTeam, Game, OverUnder, OverUnderBet, OverUnderSide, Spread, SpreadBet, SpreadSide, User


def coin_flip_multiplier(bet: CoinFlipBet):
    return 1 if bet.side == bet.coin_flip.winning_side else -1

def over_under_multiplier(bet: OverUnderBet):
    game = bet.over_under.game

    if game.home_score is None or game.away_score is None:
        raise ValueError("Game doesn't have scores submitted yet")

    total = game.home_score + game.away_score

    # Push
    if total == bet.over_under.line:
        return 0

    # Over hits
    if bet.side == OverUnderSide.OVER and total > bet.over_under.line:
        return 1

    # Under hits
    if bet.side == OverUnderSide.UNDER and total < bet.over_under.line:
        return 1

    return -1

def spread_multiplier(bet: SpreadBet):
    game = bet.spread.game

    if game.home_score is None or game.away_score is None:
        raise ValueError("Game doesn't have scores submitted yet")
    
    diff = game.home_score + bet.spread.line - game.away_score

    # Push
    if diff == 0:
        return 0

    # Home Hits
    if bet.side == SpreadSide.HOME and diff > 0:
        return 1

    # Away Hits
    if bet.side == SpreadSide.AWAY and diff < 0:
        return 1

    return -1

def league_multiplier(bet: CoinFlipBet | OverUnderBet):
    return 1.5 if bet.user.league == League.LOWER else 1

def calc_bet_winnings(bet: CoinFlipBet | OverUnderBet, bet_multiplier: Callable[[CoinFlipBet | OverUnderBet], float]):
    winnings = bet.amount * bet_multiplier(bet)
    return winnings * league_multiplier(bet) if winnings > 0 else winnings


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
        afc_wild_card_1 = Game(week=19, home_team=NflTeam.TEXANS, away_team=NflTeam.CHARGERS, home_score=32, away_score=12)
        afc_wild_card_2 = Game(week=19, home_team=NflTeam.RAVENS, away_team=NflTeam.STEELERS, home_score=28, away_score=14)
        afc_wild_card_3 = Game(week=19, home_team=NflTeam.BILLS, away_team=NflTeam.BRONCOS, home_score=31, away_score=7)

        nfc_wild_card_1 = Game(week=19, home_team=NflTeam.RAMS, away_team=NflTeam.VIKINGS, home_score=27, away_score=9)
        nfc_wild_card_2 = Game(week=19, home_team=NflTeam.BUCCANEERS, away_team=NflTeam.COMMANDERS, home_score=20, away_score=23)
        nfc_wild_card_3 = Game(week=19, home_team=NflTeam.EAGLES, away_team=NflTeam.PACKERS, home_score=22, away_score=10)
        
        # Divisional Round (Week 20)
        afc_divisional_1 = Game(week=20, home_team=NflTeam.CHIEFS, away_team=NflTeam.TEXANS, home_score=23, away_score=14)
        afc_divisional_2 = Game(week=20, home_team=NflTeam.BILLS, away_team=NflTeam.RAVENS, home_score=27, away_score=25)

        nfc_divisional_1 = Game(week=20, home_team=NflTeam.LIONS, away_team=NflTeam.COMMANDERS, home_score=31, away_score=45)
        nfc_divisional_2 = Game(week=20, home_team=NflTeam.EAGLES, away_team=NflTeam.RAMS, home_score=28, away_score=22)

        # Conference Championships (Week 21)
        afc_conference_championship = Game(week=21, home_team=NflTeam.CHIEFS, away_team=NflTeam.BILLS, home_score=32, away_score=29)
        nfc_conference_championship = Game(week=21, home_team=NflTeam.EAGLES, away_team=NflTeam.COMMANDERS, home_score=55, away_score=23)

        # Super Bowl (Week 22)
        super_bowl = Game(week=22, home_team=NflTeam.EAGLES, away_team=NflTeam.CHIEFS, home_score=40, away_score=22)

        db.add_all([
            afc_wild_card_1, afc_wild_card_2, afc_wild_card_3,
            nfc_wild_card_1, nfc_wild_card_2, nfc_wild_card_3,
            afc_divisional_1, afc_divisional_2,
            nfc_divisional_1, nfc_divisional_2,
            afc_conference_championship, nfc_conference_championship,
            super_bowl
        ])

        # Create CoinFlips
        super_bowl_coin_flip = CoinFlip(game=super_bowl, winning_side=CoinFlipSide.TAILS)
        db.add(super_bowl_coin_flip)

        # Create CoinFlipBets
        db.add(CoinFlipBet(user=max, coin_flip=super_bowl_coin_flip, side=CoinFlipSide.TAILS, amount=20))
        db.add(CoinFlipBet(user=cale, coin_flip=super_bowl_coin_flip, side=CoinFlipSide.HEADS, amount=20))

        # Create OverUnders
        afc_wild_card_1_over_under = OverUnder(game=afc_wild_card_1, line=42)
        afc_wild_card_2_over_under = OverUnder(game=afc_wild_card_2, line=43.5)
        afc_wild_card_3_over_under = OverUnder(game=afc_wild_card_3, line=47.5)
        nfc_wild_card_1_over_under = OverUnder(game=nfc_wild_card_1, line=47.5)
        nfc_wild_card_2_over_under = OverUnder(game=nfc_wild_card_2, line=50.5)
        nfc_wild_card_3_over_under = OverUnder(game=nfc_wild_card_3, line=45.5)

        afc_divisional_1_over_under = OverUnder(game=afc_divisional_1, line=41.5)
        afc_divisional_2_over_under = OverUnder(game=afc_divisional_2, line=51.5)
        nfc_divisional_1_over_under = OverUnder(game=nfc_divisional_1, line=55.5)
        nfc_divisional_2_over_under = OverUnder(game=nfc_divisional_2, line=44.5)

        afc_conference_championship_over_under = OverUnder(game=afc_conference_championship, line=47.5)
        nfc_conference_championship_over_under = OverUnder(game=nfc_conference_championship, line=47.5)
        
        db.add_all([
            afc_wild_card_1_over_under,
            afc_wild_card_2_over_under,
            afc_wild_card_3_over_under,
            nfc_wild_card_1_over_under,
            nfc_wild_card_2_over_under,
            nfc_wild_card_3_over_under,
            afc_divisional_1_over_under,
            afc_divisional_2_over_under,
            nfc_divisional_1_over_under,
            nfc_divisional_2_over_under,
            afc_conference_championship_over_under,
            nfc_conference_championship_over_under
        ])

        # Create OverUnderBets
        # Wild Card Round
        db.add(OverUnderBet(user=max, over_under=afc_wild_card_2_over_under, side=OverUnderSide.UNDER, amount=5))
        db.add(OverUnderBet(user=max, over_under=afc_wild_card_3_over_under, side=OverUnderSide.OVER, amount=5))
        db.add(OverUnderBet(user=max, over_under=nfc_wild_card_1_over_under, side=OverUnderSide.UNDER, amount=5))

        db.add(OverUnderBet(user=jesus, over_under=afc_wild_card_1_over_under, side=OverUnderSide.UNDER, amount=5))
        db.add(OverUnderBet(user=jesus, over_under=afc_wild_card_2_over_under, side=OverUnderSide.UNDER, amount=5))

        db.add(OverUnderBet(user=justin, over_under=afc_wild_card_2_over_under, side=OverUnderSide.OVER, amount=5))

        db.add(OverUnderBet(user=joey, over_under=afc_wild_card_3_over_under, side=OverUnderSide.OVER, amount=5))
        db.add(OverUnderBet(user=joey, over_under=nfc_wild_card_2_over_under, side=OverUnderSide.OVER, amount=5))

        db.add(OverUnderBet(user=mason, over_under=afc_wild_card_1_over_under, side=OverUnderSide.UNDER, amount=5))
        db.add(OverUnderBet(user=mason, over_under=afc_wild_card_2_over_under, side=OverUnderSide.UNDER, amount=5))
        db.add(OverUnderBet(user=mason, over_under=afc_wild_card_3_over_under, side=OverUnderSide.OVER, amount=5))
        db.add(OverUnderBet(user=mason, over_under=nfc_wild_card_1_over_under, side=OverUnderSide.UNDER, amount=5))
        db.add(OverUnderBet(user=mason, over_under=nfc_wild_card_2_over_under, side=OverUnderSide.OVER, amount=5))
        db.add(OverUnderBet(user=mason, over_under=nfc_wild_card_3_over_under, side=OverUnderSide.OVER, amount=5))

        db.add(OverUnderBet(user=asher, over_under=afc_wild_card_3_over_under, side=OverUnderSide.OVER, amount=5))

        db.add(OverUnderBet(user=ben, over_under=afc_wild_card_1_over_under, side=OverUnderSide.UNDER, amount=5))
        db.add(OverUnderBet(user=ben, over_under=nfc_wild_card_3_over_under, side=OverUnderSide.UNDER, amount=5))

        # Divisional Round
        db.add(OverUnderBet(user=mason, over_under=nfc_divisional_1_over_under, side=OverUnderSide.OVER, amount=5))
        db.add(OverUnderBet(user=mason, over_under=nfc_divisional_2_over_under, side=OverUnderSide.UNDER, amount=5))

        db.add(OverUnderBet(user=max, over_under=afc_divisional_2_over_under, side=OverUnderSide.UNDER, amount=5))

        db.add(OverUnderBet(user=asher, over_under=nfc_divisional_1_over_under, side=OverUnderSide.OVER, amount=5))

        db.add(OverUnderBet(user=justin, over_under=afc_divisional_2_over_under, side=OverUnderSide.OVER, amount=5))
        db.add(OverUnderBet(user=justin, over_under=nfc_divisional_1_over_under, side=OverUnderSide.UNDER, amount=5))

        db.add(OverUnderBet(user=mikey, over_under=nfc_divisional_1_over_under, side=OverUnderSide.OVER, amount=5))

        db.add(OverUnderBet(user=ben, over_under=afc_divisional_1_over_under, side=OverUnderSide.UNDER, amount=5))
        db.add(OverUnderBet(user=ben, over_under=afc_divisional_2_over_under, side=OverUnderSide.OVER, amount=5))

        db.add(OverUnderBet(user=joey, over_under=nfc_divisional_1_over_under, side=OverUnderSide.OVER, amount=5))
        db.add(OverUnderBet(user=joey, over_under=afc_divisional_1_over_under, side=OverUnderSide.UNDER, amount=5))

        db.add(OverUnderBet(user=jesus, over_under=nfc_divisional_1_over_under, side=OverUnderSide.UNDER, amount=5))

        # Conference Championships
        db.add(OverUnderBet(user=max, over_under=afc_conference_championship_over_under, side=OverUnderSide.UNDER, amount=5))
        db.add(OverUnderBet(user=joey, over_under=nfc_conference_championship_over_under, side=OverUnderSide.OVER, amount=5))

        # Create Spreads
        afc_wild_card_1_spread = Spread(game=afc_wild_card_1, line=3)
        afc_wild_card_2_spread = Spread(game=afc_wild_card_2, line=-10)
        afc_wild_card_3_spread = Spread(game=afc_wild_card_3, line=-9)

        nfc_wild_card_1_spread = Spread(game=nfc_wild_card_1, line=2.5)
        nfc_wild_card_2_spread = Spread(game=nfc_wild_card_2, line=-3)
        nfc_wild_card_3_spread = Spread(game=nfc_wild_card_3, line=-5)

        afc_divisional_1_spread = Spread(game=afc_divisional_1, line=-8.5)
        afc_divisional_2_spread = Spread(game=afc_divisional_2, line=1)

        nfc_divisional_1_spread = Spread(game=nfc_divisional_1, line=-9.5)
        nfc_divisional_2_spread = Spread(game=nfc_divisional_2, line=-6)

        afc_conference_championship_spread = Spread(game=afc_conference_championship, line=-2)
        nfc_conference_championship_spread = Spread(game=nfc_conference_championship, line=-6)

        super_bowl_spread = Spread(game=super_bowl, line=1.5)

        db.add_all([
            afc_wild_card_1_spread, afc_wild_card_2_spread, afc_wild_card_3_spread,
            nfc_wild_card_1_spread, nfc_wild_card_2_spread, nfc_wild_card_3_spread,
            afc_divisional_1_spread, afc_divisional_2_spread,
            nfc_divisional_1_spread, nfc_divisional_2_spread,
            afc_conference_championship_spread, nfc_conference_championship_spread,
            super_bowl_spread
        ])

        # Create SpreadBets
        # Wild Card Round
        db.add(SpreadBet(user=max, spread=afc_wild_card_1_spread, side=SpreadSide.AWAY, amount=5))
        db.add(SpreadBet(user=max, spread=nfc_wild_card_3_spread, side=SpreadSide.HOME, amount=5))

        db.add(SpreadBet(user=justin, spread=nfc_wild_card_1_spread, side=SpreadSide.AWAY, amount=5))
        db.add(SpreadBet(user=justin, spread=nfc_wild_card_2_spread, side=SpreadSide.AWAY, amount=5))
        db.add(SpreadBet(user=justin, spread=nfc_wild_card_3_spread, side=SpreadSide.AWAY, amount=5))
        db.add(SpreadBet(user=justin, spread=afc_wild_card_3_spread, side=SpreadSide.AWAY, amount=5))
        db.add(SpreadBet(user=justin, spread=afc_wild_card_1_spread, side=SpreadSide.AWAY, amount=5))

        db.add(SpreadBet(user=jesus, spread=nfc_wild_card_1_spread, side=SpreadSide.AWAY, amount=5))

        db.add(SpreadBet(user=joey, spread=nfc_wild_card_1_spread, side=SpreadSide.AWAY, amount=5))

        db.add(SpreadBet(user=asher, spread=afc_wild_card_1_spread, side=SpreadSide.AWAY, amount=5))
        db.add(SpreadBet(user=asher, spread=nfc_wild_card_2_spread, side=SpreadSide.AWAY, amount=5))

        db.add(SpreadBet(user=ben, spread=afc_wild_card_2_spread, side=SpreadSide.HOME, amount=5))
        db.add(SpreadBet(user=ben, spread=afc_wild_card_3_spread, side=SpreadSide.AWAY, amount=5))
        db.add(SpreadBet(user=ben, spread=nfc_wild_card_1_spread, side=SpreadSide.HOME, amount=5))
        db.add(SpreadBet(user=ben, spread=nfc_wild_card_2_spread, side=SpreadSide.HOME, amount=5))

        # Divisional Round
        db.add(SpreadBet(user=mason, spread=afc_divisional_1_spread, side=SpreadSide.AWAY, amount=5))
        db.add(SpreadBet(user=mason, spread=afc_divisional_2_spread, side=SpreadSide.HOME, amount=5))

        db.add(SpreadBet(user=max, spread=afc_divisional_1_spread, side=SpreadSide.AWAY, amount=5))
        db.add(SpreadBet(user=max, spread=nfc_divisional_1_spread, side=SpreadSide.HOME, amount=5))
        db.add(SpreadBet(user=max, spread=nfc_divisional_2_spread, side=SpreadSide.HOME, amount=5))

        db.add(SpreadBet(user=asher, spread=afc_divisional_1_spread, side=SpreadSide.HOME, amount=5))

        db.add(SpreadBet(user=justin, spread=afc_divisional_1_spread, side=SpreadSide.HOME, amount=5))
        db.add(SpreadBet(user=justin, spread=nfc_divisional_2_spread, side=SpreadSide.HOME, amount=5))

        db.add(SpreadBet(user=mikey, spread=afc_divisional_1_spread, side=SpreadSide.AWAY, amount=5))
        db.add(SpreadBet(user=mikey, spread=nfc_divisional_2_spread, side=SpreadSide.AWAY, amount=5))
        db.add(SpreadBet(user=mikey, spread=afc_divisional_2_spread, side=SpreadSide.HOME, amount=5))

        db.add(SpreadBet(user=ben, spread=nfc_divisional_1_spread, side=SpreadSide.AWAY, amount=5))
        db.add(SpreadBet(user=ben, spread=nfc_divisional_2_spread, side=SpreadSide.HOME, amount=5))

        db.add(SpreadBet(user=joey, spread=afc_divisional_2_spread, side=SpreadSide.HOME, amount=5))

        db.add(SpreadBet(user=cale, spread=afc_divisional_1_spread, side=SpreadSide.HOME, amount=5))
        db.add(SpreadBet(user=cale, spread=afc_divisional_2_spread, side=SpreadSide.AWAY, amount=5))
        db.add(SpreadBet(user=cale, spread=nfc_divisional_1_spread, side=SpreadSide.AWAY, amount=5))
        db.add(SpreadBet(user=cale, spread=nfc_divisional_2_spread, side=SpreadSide.AWAY, amount=5))

        db.add(SpreadBet(user=jesus, spread=nfc_divisional_2_spread, side=SpreadSide.HOME, amount=5))
        db.add(SpreadBet(user=jesus, spread=afc_divisional_2_spread, side=SpreadSide.AWAY, amount=5))

        # Conference Championships
        db.add(SpreadBet(user=mason, spread=afc_conference_championship_spread, side=SpreadSide.AWAY, amount=5))
        db.add(SpreadBet(user=mason, spread=nfc_conference_championship_spread, side=SpreadSide.AWAY, amount=5))

        db.add(SpreadBet(user=ben, spread=afc_conference_championship_spread, side=SpreadSide.HOME, amount=5))
        db.add(SpreadBet(user=ben, spread=nfc_conference_championship_spread, side=SpreadSide.HOME, amount=5))

        db.add(SpreadBet(user=justin, spread=afc_conference_championship_spread, side=SpreadSide.AWAY, amount=5))
        db.add(SpreadBet(user=justin, spread=nfc_conference_championship_spread, side=SpreadSide.AWAY, amount=5))

        db.add(SpreadBet(user=asher, spread=nfc_conference_championship_spread, side=SpreadSide.AWAY, amount=5))

        db.add(SpreadBet(user=max, spread=nfc_conference_championship_spread, side=SpreadSide.HOME, amount=5))

        db.add(SpreadBet(user=mikey, spread=nfc_conference_championship_spread, side=SpreadSide.HOME, amount=5))
        db.add(SpreadBet(user=mikey, spread=afc_conference_championship_spread, side=SpreadSide.AWAY, amount=5))

        db.add(SpreadBet(user=jesus, spread=afc_conference_championship_spread, side=SpreadSide.HOME, amount=5))
        db.add(SpreadBet(user=jesus, spread=nfc_conference_championship_spread, side=SpreadSide.HOME, amount=5))

        db.add(SpreadBet(user=joey, spread=afc_conference_championship_spread, side=SpreadSide.AWAY, amount=5))


        # Super Bowl
        db.add(SpreadBet(user=cale, spread=super_bowl_spread, side=SpreadSide.AWAY, amount=20))
        db.add(SpreadBet(user=justin, spread=super_bowl_spread, side=SpreadSide.HOME, amount=20))
        db.add(SpreadBet(user=max, spread=super_bowl_spread, side=SpreadSide.AWAY, amount=20))
        db.add(SpreadBet(user=mikey, spread=super_bowl_spread, side=SpreadSide.AWAY, amount=20))
        db.add(SpreadBet(user=ben, spread=super_bowl_spread, side=SpreadSide.AWAY, amount=20))
        db.add(SpreadBet(user=asher, spread=super_bowl_spread, side=SpreadSide.HOME, amount=20))

        db.commit()

        # Calculate winnings per user
        for user in [max, cale, jesus, justin, joey, mason, asher, ben, mikey, aaron]:
            winnings = 0
            for bet in user.coin_flip_bets:
                winnings += calc_bet_winnings(bet, coin_flip_multiplier)

            for bet in user.over_under_bets:
                winnings += calc_bet_winnings(bet, over_under_multiplier)

            for bet in user.spread_bets:
                winnings += calc_bet_winnings(bet, spread_multiplier)

            print(f"{user.name} won {winnings} dollars total")

    finally:
        # Make sure to close the session properly
        try:
            next(session_generator)  # This triggers the code after yield
        except StopIteration:
            pass
