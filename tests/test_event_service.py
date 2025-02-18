from datetime import datetime, date, time, timedelta

import pytest

from src.models import User, Executor, Event, RecurrentEvent


def create_user_and_executor(db_session, name="Default User", role="teacher"):
    """Creates a user and an executor and returns them."""
    executor = Executor()
    user = User(name=name, role=role, executor_id=executor.id)
    db_session.add_all([user, executor])
    db_session.commit()
    return user, executor


def test_create_non_colliding_events(event_service, db_session):
    """Ensures events do not collide when they belong to different executors."""
    user1, executor1 = create_user_and_executor(db_session, "Alice")
    user2, executor2 = create_user_and_executor(db_session, "Bob")

    # Create two events at the same time, but different executors
    event1 = event_service.add_event(user1, executor1, "Math", time(10, 0), time(11, 0), date.today())
    event2 = event_service.add_event(user2, executor2, "Physics", time(10, 0), time(11, 0), date.today())

    assert event1 is not None
    assert event2 is not None
    assert event1.executor_id != event2.executor_id  # Different executors


def test_prevent_event_collision(event_service, db_session):
    """Ensures that two events cannot be scheduled at the same time for the same executor."""
    user1, executor1 = create_user_and_executor(db_session, "Alice")

    # Create an event
    event1 = event_service.add_event(user1, executor1, "History", time(9, 0), time(10, 0), date.today())

    # Attempt to create a colliding event
    with pytest.raises(ValueError):
        event_service.add_event(user1, executor1, "Science", time(9, 30), time(10, 30), date.today())


def test_create_recurrent_event(event_service, db_session):
    """Ensures a recurrent event can be created."""
    user1, executor1 = create_user_and_executor(db_session, "Charlie")

    recurrent_event = event_service.add_event(
        user1, executor1, "Weekly Math", time(14, 0), time(15, 0), date.today(),
        interval=timedelta(days=7), start=datetime.now(), end=datetime.now() + timedelta(weeks=4)
    )

    assert recurrent_event is not None
    assert recurrent_event.event is not None  # Ensures recurrent event is created


def test_prevent_recurrent_event_collision(event_service, db_session):
    """Ensures that recurrent events cannot collide with existing events of the same executor."""
    user1, executor1 = create_user_and_executor(db_session, "David")

    # Create a weekly recurring event
    event_service.add_event(
        user1, executor1, "Weekly Physics", time(12, 0), time(13, 0), date.today(),
        interval=timedelta(days=7), start=datetime.now(), end=datetime.now() + timedelta(weeks=4)
    )

    # Attempt to create another overlapping recurrent event
    with pytest.raises(ValueError):
        event_service.add_event(
            user1, executor1, "Weekly Chemistry", time(12, 30), time(13, 30), date.today(),
            interval=timedelta(days=7), start=datetime.now(), end=datetime.now() + timedelta(weeks=4)
        )


def test_cancel_event(event_service, db_session):
    """Ensures an event can be canceled."""
    user1, executor1 = create_user_and_executor(db_session, "Eve")

    event = event_service.add_event(user1, executor1, "Biology", time(16, 0), time(17, 0), date.today())

    canceled_event = event_service.cancel_event(event)
    db_session.commit()

    assert canceled_event.cancelled is True


def test_move_event(event_service, db_session):
    """Ensures an event can be moved to a new time slot."""
    user1, executor1 = create_user_and_executor(db_session, "Frank")

    event = event_service.add_event(user1, executor1, "English", time(8, 0), time(9, 0), date.today())

    # Move the event
    moved_event = event_service.move_event(event, new_st=time(10, 0), new_et=time(11, 0))
    db_session.commit()

    assert moved_event.start_time == time(10, 0)
    assert moved_event.end_time == time(11, 0)


def test_get_events_for_day(event_service, db_session):
    """Ensures the service retrieves all events for a day."""
    user1, executor1 = create_user_and_executor(db_session, "George")

    event_service.add_event(user1, "Art", time(13, 0), time(14, 0), date.today())

    events = event_service.events_for_day(date.today(), user1)
    assert len(events) == 1
    assert events[0].event_type == "Art"


def test_get_available_slots(event_service, db_session):
    """Ensures available slots are calculated correctly."""
    user1, executor1 = create_user_and_executor(db_session, "Helen")

    # Create an event from 10:00 to 11:00
    event_service.add_event(user1, "French", time(10, 0), time(11, 0), date.today())

    available_slots = event_service.available_slots(executor1, datetime.combine(date.today(), time(9, 0)),
                                                    datetime.combine(date.today(), time(12, 0)), timedelta(minutes=30))

    assert len(available_slots) > 0
    assert (time(9, 0), time(9, 30)) in available_slots
    assert (time(9, 30), time(10, 0)) in available_slots
    assert (time(11, 0), time(11, 30)) in available_slots
