from time import sleep

from loguru import logger

from db.connection import BaseStorage
from errors.errors import DeleteNotExistsObjectError


class AtomicTransaction:
    __level: int = 0
    __in_working = False

    def __init__(self):
        while self.__in_working:
            sleep(1)
        self.__in_working = True
        BaseStorage.start_transaction()

    def begin(self, *operations):
        operations_count = 0
        try:
            for operation, params in operations:
                try:
                    operation(**{"in_transaction": True, **params})
                except DeleteNotExistsObjectError:
                    logger.info('try to delete not exists object')
                    continue
                operations_count += 1

        except Exception as error:
            logger.info(f'{error}')
            if self.__level == 1:
                BaseStorage.failed_transaction()
            else:
                BaseStorage.cancel_operations(operations_count)

    @staticmethod
    def __execute():
        BaseStorage.end_transaction()

    def __enter__(self):
        self.__level += 1
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.__level >= 1:
            self.__level -= 1

        if not self.__level:
            self.__execute()
            self.__in_working = False
