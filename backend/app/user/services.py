from app.models import Interests, Users, TripPurposes, Arrivals, Departures


DEFAULT_CHUNK_SIZE = 1024 * 1024 * 1  # 1 megabyte


def calculate_soulmate_score(db, user1: Users, user2: Users):
    score = 0

    user1_interests = db.query(Interests).filter(Interests.users.any(id=user1.id)).all()
    user2_interests = db.query(Interests).filter(Interests.users.any(id=user2.id)).all()
    matching_interests = len(set(user1_interests) & set(user2_interests))
    score += matching_interests

    user1_trip_purposes = (
        db.query(TripPurposes).filter(TripPurposes.users.any(id=user1.id)).all()
    )
    user2_trip_purposes = (
        db.query(TripPurposes).filter(TripPurposes.users.any(id=user2.id)).all()
    )
    matching_trip_purposes = len(set(user1_trip_purposes) & set(user2_trip_purposes))
    score += matching_trip_purposes

    user1_departures = (
        db.query(Departures).filter(Departures.users.any(id=user1.id)).all()
    )
    user2_departures = (
        db.query(Departures).filter(Departures.users.any(id=user2.id)).all()
    )
    matching_departures = len(set(user1_departures) & set(user2_departures))
    score += matching_departures * 2

    user1_arrivals = db.query(Arrivals).filter(Arrivals.users.any(id=user1.id)).all()
    user2_arrivals = db.query(Arrivals).filter(Arrivals.users.any(id=user2.id)).all()
    matching_arrivals = len(set(user1_arrivals) & set(user2_arrivals))
    score += matching_arrivals * 2

    return score
