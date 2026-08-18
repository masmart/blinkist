from contextlib import contextmanager

from config import db


@contextmanager
def transaction():
    """Commit one use case atomically and always rollback on failure."""
    try:
        yield db.session
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise
