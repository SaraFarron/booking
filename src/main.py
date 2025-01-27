from datetime import datetime, timedelta as td

from sqlalchemy.orm import Session

from database import engine
from models import User, Executor
from repositories import UserRepo, EventRepo, RecurrentEventRepo, EventBreakRepo

with Session(engine) as session:
    user = User(name="test", role="user")
    session.add(user)

    executor = Executor()
    session.add(executor)
    session.commit()

    user = User(name="test2", role="admin", executor_id=executor.id)
    session.add(user)
    session.commit()

    user = UserRepo(session).get(1)

    now = datetime.now()
    now_time = now.time()
    now_and_hour_time = now_time.replace(hour=now.hour + 1)

    event = EventRepo(session).new(user, executor, "lesson", now_time, now_and_hour_time, now.date())
    session.add(event)

    event_break = EventBreakRepo(session).new(
        user, "weekend", now + td(days=3), now + td(days=7),
    )
    session.add(event_break)

    recurrent_event = RecurrentEventRepo(session).new(
        user,
        executor,
        "lesson",
        now_time,
        now_and_hour_time,
        now.date(),
        td(weeks=1),
        now,
        now + td(days=7),
    )

    session.commit()
