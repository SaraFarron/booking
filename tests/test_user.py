from src.models import User


def test_create_user(db_session):
    """Test user creation in the database."""
    user = User(name="Alice")
    db_session.add(user)
    db_session.commit()

    # Fetch user from the database
    retrieved_user = db_session.query(User).filter_by(name="Alice").first()

    assert retrieved_user is not None
    assert retrieved_user.name == "Alice"


def test_empty_database(db_session):
    """Test that the database is empty at the start."""
    users = db_session.query(User).all()
    assert len(users) == 0
