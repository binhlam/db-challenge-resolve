# -*- coding: utf-8 -*-
from configuration import ConfigManager
from pkg.db.database import ConnectionPool


def run():
    # init config
    config = ConfigManager()
    logger = config.init_logger()
    logger.info('Logger initialized')

    # init connection pool
    connection_pool = ConnectionPool()
    connection_pool.init_pool(config)

    # init app
    from app import flask_app
    return flask_app


if __name__ == "__main__":
    run()
