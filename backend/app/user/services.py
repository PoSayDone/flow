from app.models import Interests, Users, TripPurposes, Arrivals, Departures


DEFAULT_CHUNK_SIZE = 1024 * 1024 * 1  # 1 megabyte


def calculate_soulmate_score(db, user1: Users, user2: Users):
    score = 0

    ### Interests

    user1_interests = db.query(Interests).filter(Interests.users.any(id=user1.id)).all()
    user2_interests = db.query(Interests).filter(Interests.users.any(id=user2.id)).all()
    matching_interests = len(set(user1_interests) & set(user2_interests))
    score += matching_interests

    ### TripPurposes

    user1_trip_purposes = (
        db.query(TripPurposes).filter(TripPurposes.users.any(id=user1.id)).all()
    )
    user2_trip_purposes = (
        db.query(TripPurposes).filter(TripPurposes.users.any(id=user2.id)).all()
    )
    matching_trip_purposes = len(set(user1_trip_purposes) & set(user2_trip_purposes))
    score += matching_trip_purposes

    ### Departures

    user1_departures = (
        db.query(Departures).filter(Departures.users.any(id=user1.id)).all()
    )
    user2_departures = (
        db.query(Departures).filter(Departures.users.any(id=user2.id)).all()
    )

    all_departures = False
    if user2_departures and user2_departures[0].id == 1:
        all_departures = True

    if all_departures:
        score += 3 * 2
    else:
        matching_departures = len(set(user1_departures) & set(user2_departures))
        score += matching_departures * 2

    ### Arrivals

    user1_arrivals = db.query(Arrivals).filter(Arrivals.users.any(id=user1.id)).all()
    user2_arrivals = db.query(Arrivals).filter(Arrivals.users.any(id=user2.id)).all()

    all_arrivals = False
    if user2_arrivals and user2_arrivals[0].id == 1:
        all_arrivals = True

    if all_arrivals:
        score += 3 * 2
    else:
        matching_arrivals = len(set(user1_arrivals) & set(user2_arrivals))
        score += matching_arrivals * 2

    return score
