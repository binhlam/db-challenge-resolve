from app.repository.generator import GeneratorRepository


class Repository(
    GeneratorRepository,
):
    def __init__(self, pool=None, logger=None):
        self.pool = pool
        self.logger = logger
