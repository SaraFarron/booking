from datetime import datetime, timedelta
from database import engine
from sqlalchemy.orm import Session
from repositories import UserRepo, EventRepo, RecurrentEventRepo, EventBreakRepo
from models import User, Event, EventBreak, RecurrentEvent, Executor

with Session(engine) as session:
    user = User(name="test", role="user")
    session.add(user)
    session.commit()

    executor = Executor()
    session.add(executor)

    user = User(name="test2", role="admin", executor_id=executor.id)
    session.add(user)

    user = UserRepo(session).get(1)
    now = datetime.now()
    event = Event(
        user_id=user.user_id,
        event_type="lesson",
        start_time=now.time(),
        end_time=now.time().replace(hour=now.hour + 1),
        date=now.date(),
        weekday=now.weekday(),
    )
    session.add(event)

    event_break = EventBreak(
        user_id=user.user_id,
        break_type="weekend",
        start=now + timedelta(days=3),
        end=now + timedelta(days=7),
    )
    session.add(event_break)

    recurrent_event = RecurrentEventRepo(session).new(
        user=user,
        executor=executor,
        event_type="lesson",
        start_time=now.time(),
        end_time=now.time().replace(hour=now.hour + 1),
        day=now.date(),
        interval=timedelta(weeks=1),
        start=now,
        end=now + timedelta(days=7),
    )

    session.commit()
