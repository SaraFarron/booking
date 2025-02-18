from datetime import datetime, time, date, timedelta
from datetime import datetime, time, date, timedelta

from src.models import User, Executor, Event, RecurrentEvent, EventBreak


def test_create_user(db_session):
    """Test creating a user."""
    user = User(name="John Doe", role="admin")
    db_session.add(user)
    db_session.commit()

    fetched_user = db_session.query(User).filter_by(name="John Doe").first()
    assert fetched_user is not None
    assert fetched_user.name == "John Doe"
    assert fetched_user.role == "admin"


def test_create_executor(db_session):
    """Test creating an executor."""
    executor = Executor()
    db_session.add(executor)
    db_session.commit()

    fetched_executor = db_session.query(Executor).first()
    assert fetched_executor is not None
    assert fetched_executor.id is not None


def test_create_event(db_session):
    """Test creating an event."""
    user = User(name="Alice", role="user")
    executor = Executor()
    db_session.add_all([user, executor])
    db_session.commit()

    event = Event(
        user_id=user.id,
        executor_id=executor.id,
        event_type="Meeting",
        start_time=time(9, 0),
        end_time=time(10, 0),
        date=date.today(),
        weekday=datetime.today().weekday(),
        cancelled=False
    )
    db_session.add(event)
    db_session.commit()

    fetched_event = db_session.query(Event).first()
    assert fetched_event is not None
    assert fetched_event.event_type == "Meeting"


def test_update_event(db_session):
    """Test updating an event."""
    user = User(name="Bob", role="user")
    executor = Executor()
    db_session.add_all([user, executor])
    db_session.commit()

    event = Event(
        user_id=user.id,
        executor_id=executor.id,
        event_type="Conference",
        start_time=time(14, 0),
        end_time=time(15, 0),
        date=date.today(),
        weekday=datetime.today().weekday()
    )
    db_session.add(event)
    db_session.commit()

    # Update event
    event.cancelled = True
    db_session.commit()

    fetched_event = db_session.query(Event).first()
    assert fetched_event.cancelled is True


def test_delete_event(db_session):
    """Test deleting an event."""
    user = User(name="Charlie", role="user")
    executor = Executor()
    db_session.add_all([user, executor])
    db_session.commit()

    event = Event(
        user_id=user.id,
        executor_id=executor.id,
        event_type="Workshop",
        start_time=time(16, 0),
        end_time=time(17, 0),
        date=date.today(),
        weekday=datetime.today().weekday()
    )
    db_session.add(event)
    db_session.commit()

    db_session.delete(event)
    db_session.commit()

    fetched_event = db_session.query(Event).first()
    assert fetched_event is None




def test_create_recurrent_event(db_session):
    """Test creating a recurrent event."""
    user = User(name="David", role="manager")
    executor = Executor()
    db_session.add_all([user, executor])
    db_session.commit()

    event = Event(
        user_id=user.id,
        executor_id=executor.id,
        event_type="Weekly Meeting",
        start_time=time(10, 0),
        end_time=time(11, 0),
        date=date.today(),
        weekday=datetime.today().weekday()
    )
    db_session.add(event)
    db_session.commit()

    recurrent_event = RecurrentEvent(
        user_id=user.id,
        executor_id=executor.id,
        event_id=event.id,
        interval=7,  # Weekly recurrence
        start=datetime.now(),
        end=datetime.now() + timedelta(weeks=4)  # Repeats for 4 weeks
    )
    db_session.add(recurrent_event)
    db_session.commit()

    fetched_recurrent_event = db_session.query(RecurrentEvent).first()
    assert fetched_recurrent_event is not None
    assert fetched_recurrent_event.interval == 7
    assert fetched_recurrent_event.event_id == event.id


def test_update_recurrent_event(db_session):
    """Test updating a recurrent event interval."""
    user = User(name="Emma", role="staff")
    executor = Executor()
    db_session.add_all([user, executor])
    db_session.commit()

    event = Event(
        user_id=user.id,
        executor_id=executor.id,
        event_type="Monthly Review",
        start_time=time(15, 0),
        end_time=time(16, 0),
        date=date.today(),
        weekday=datetime.today().weekday()
    )
    db_session.add(event)
    db_session.commit()

    recurrent_event = RecurrentEvent(
        user_id=user.id,
        executor_id=executor.id,
        event_id=event.id,
        interval=30,  # Monthly recurrence
        start=datetime.now(),
        end=datetime.now() + timedelta(days=90)  # Repeats for 3 months
    )
    db_session.add(recurrent_event)
    db_session.commit()

    # Update recurrence interval
    recurrent_event.interval = 14  # Change to bi-weekly
    db_session.commit()

    fetched_recurrent_event = db_session.query(RecurrentEvent).first()
    assert fetched_recurrent_event.interval == 14


def test_delete_recurrent_event(db_session):
    """Test deleting a recurrent event."""
    user = User(name="Frank", role="developer")
    executor = Executor()
    db_session.add_all([user, executor])
    db_session.commit()

    event = Event(
        user_id=user.id,
        executor_id=executor.id,
        event_type="Daily Standup",
        start_time=time(9, 30),
        end_time=time(9, 45),
        date=date.today(),
        weekday=datetime.today().weekday()
    )
    db_session.add(event)
    db_session.commit()

    recurrent_event = RecurrentEvent(
        user_id=user.id,
        executor_id=executor.id,
        event_id=event.id,
        interval=1,  # Daily recurrence
        start=datetime.now(),
        end=datetime.now() + timedelta(days=30)  # Repeats for 30 days
    )
    db_session.add(recurrent_event)
    db_session.commit()

    db_session.delete(recurrent_event)
    db_session.commit()

    fetched_recurrent_event = db_session.query(RecurrentEvent).first()
    assert fetched_recurrent_event is None


def test_create_event_break(db_session):
    """Test creating an event break."""
    user = User(name="Grace", role="engineer")
    db_session.add(user)
    db_session.commit()

    event_break = EventBreak(
        user_id=user.id,
        break_type="Lunch",
        start=datetime.now(),
        end=datetime.now() + timedelta(hours=1)
    )
    db_session.add(event_break)
    db_session.commit()

    fetched_break = db_session.query(EventBreak).first()
    assert fetched_break is not None
    assert fetched_break.break_type == "Lunch"


def test_update_event_break(db_session):
    """Test updating an event break."""
    user = User(name="Helen", role="designer")
    db_session.add(user)
    db_session.commit()

    event_break = EventBreak(
        user_id=user.id,
        break_type="Coffee Break",
        start=datetime.now(),
        end=datetime.now() + timedelta(minutes=15)
    )
    db_session.add(event_break)
    db_session.commit()

    # Update break duration
    event_break.end = event_break.start + timedelta(minutes=30)
    db_session.commit()

    fetched_break = db_session.query(EventBreak).first()
    assert (fetched_break.end - fetched_break.start).seconds == 1800  # 30 min


def test_delete_event_break(db_session):
    """Test deleting an event break."""
    user = User(name="Ian", role="analyst")
    db_session.add(user)
    db_session.commit()

    event_break = EventBreak(
        user_id=user.id,
        break_type="Short Break",
        start=datetime.now(),
        end=datetime.now() + timedelta(minutes=10)
    )
    db_session.add(event_break)
    db_session.commit()

    db_session.delete(event_break)
    db_session.commit()

    fetched_break = db_session.query(EventBreak).first()
    assert fetched_break is None
