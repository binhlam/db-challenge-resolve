from pkg.db.database import _pool
from contextlib import contextmanager
import logging

_logger = logging.getLogger('db-challenge')


@contextmanager
def transaction(name="transaction", **kwargs):
    # Get the session parameters from the kwargs
    options = {
        "isolation_level": kwargs.get("isolation_level", None),
        "readonly": kwargs.get("readonly", None),
        "deferrable": kwargs.get("deferrable", None),
    }
    conn = None
    try:
        conn = _pool.getconn()
        conn.set_session(**options)
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        _logger.error("{} error: {}".format(name, e))
    finally:
        conn.reset()
        _pool.putconn(conn)
