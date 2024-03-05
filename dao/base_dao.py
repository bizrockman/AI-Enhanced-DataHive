from typing import Type, Union
from datetime import datetime

from models import DataHiveBaseModel


class BaseDAO:
    def create(self, entity: DataHiveBaseModel) -> DataHiveBaseModel:
        raise NotImplementedError

    def read(self, entity: Type[DataHiveBaseModel], filters=None, limit=None, order_by=None, order_dir='asc') -> (
            Union)[Type[DataHiveBaseModel], list[Type[DataHiveBaseModel]]]:
        raise NotImplementedError

    def update(self, entity: DataHiveBaseModel, id=None) -> DataHiveBaseModel:
        raise NotImplementedError

    def delete(self, entity: DataHiveBaseModel, id=None):
        raise NotImplementedError

    def get_latest_entity_date(self, entity: Type[DataHiveBaseModel], creator_name: str) -> Union[datetime, None]:
        entity = self.read(entity, filters=[['creator', creator_name]], order_by='created_at', order_dir='desc',
                             limit=1)

        if entity:
            entity = entity[0]
            return entity.created_at
        else:
            return None
