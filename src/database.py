from sqlalchemy import create_engine

from loguru import logger
from models import Base

logger.info("Connecting to DB")
engine = create_engine("sqlite:///../db/db.sqlite")
Base.metadata.create_all(engine)
