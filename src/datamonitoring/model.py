# coding=utf-8
import decimal
import enum
from datetime import date, datetime
from enum import Enum
from typing import Dict

from .dateutils import localize


@enum.unique
class DataUnit(Enum):
    B = 0
    KB = 1
    MB = 2
    GB = 3
    TB = 4

    @property
    def multiplier(self):
        return 1024 ** self.value


class DataAmount:

    def __init__(self, amount: decimal.Decimal, unit: DataUnit):
        self._nb_bytes = amount * unit.multiplier

    def __add__(self, other):
        if isinstance(other, DataAmount):
            return DataAmount(self._nb_bytes + other._nb_bytes, DataUnit.B)
        else:
            raise TypeError("Cannot add a {type1} to a {type2}".format(type1=type(other), type2=type(self)))

    def __sub__(self, other):
        if isinstance(other, DataAmount):
            return DataAmount(self._nb_bytes - other._nb_bytes, DataUnit.B)
        else:
            raise TypeError("Cannot substract a {type1} to a {type2}".format(type1=type(other), type2=type(self)))

    def __truediv__(self, other):
        if isinstance(other, DataAmount):
            return self._nb_bytes / other._nb_bytes
        else:
            raise TypeError("Cannot divide a {type1} by a {type2}".format(type1=type(self), type2=type(other)))

    def __le__(self, other):
        if isinstance(other, DataAmount):
            return self._nb_bytes <= other._nb_bytes
        else:
            raise TypeError("Cannot compare a {type1} with a {type2}".format(type1=type(self), type2=type(other)))

    def __lt__(self, other):
        if isinstance(other, DataAmount):
            return self._nb_bytes < other._nb_bytes
        else:
            raise TypeError("Cannot compare a {type1} with a {type2}".format(type1=type(self), type2=type(other)))

    def __gt__(self, other):
        if isinstance(other, DataAmount):
            return self._nb_bytes > other._nb_bytes
        else:
            raise TypeError("Cannot compare a {type1} with a {type2}".format(type1=type(self), type2=type(other)))

    def __ge__(self, other):
        if isinstance(other, DataAmount):
            return self._nb_bytes >= other._nb_bytes
        else:
            raise TypeError("Cannot compare a {type1} with a {type2}".format(type1=type(self), type2=type(other)))

    def __eq__(self, other):
        if isinstance(other, DataAmount):
            return self._nb_bytes == other._nb_bytes
        else:
            raise TypeError("Cannot compare a {type1} with a {type2}".format(type1=type(self), type2=type(other)))

    def __repr__(self):
        return "{:g} GB".format(self.get_value(DataUnit.GB))

    def get_value(self, unit: DataUnit):
        return self._nb_bytes / unit.multiplier


class ModelBase:
    _TABLE = None

    def __init__(self, id: int = None):
        self._id = id

    @property
    def table_name(self):
        return self._TABLE

    @property
    def id(self):
        return self._id

    def _set_id(self, value):
        self._id = id

    @property
    def has_id(self):
        return self.id is not None

    @staticmethod
    def from_dict(data: Dict):
        raise NotImplementedError()

    def to_dict(self):
        raise NotImplementedError()


class Usage(ModelBase):
    _TABLE = 'usage'

    def __init__(self,
                 period_start: date,
                 period_end: date,
                 phone_number: str,
                 quota_name: str,
                 created: datetime,
                 updated: datetime,
                 used_gb: float,
                 limit_gb: float,
                 id: int = None):
        super().__init__(id)
        self._period_start = period_start
        self._period_end = period_end
        self._created = localize(created)
        self._updated = localize(updated)
        self._phone_number = phone_number
        self._used_gb = used_gb
        self._quota_name = quota_name
        self._limit_gb = limit_gb

    @property
    def period_start(self) -> date:
        return self._period_start

    @property
    def period_end(self) -> date:
        return self._period_end

    @property
    def quota_name(self) -> str:
        return self._quota_name

    @property
    def updated(self) -> datetime:
        return self._updated

    @property
    def created(self) -> datetime:
        return self._created

    @property
    def used_gb(self) -> float:
        return self._used_gb

    @property
    def phone_number(self) -> str:
        return self._phone_number

    @property
    def limit_gb(self) -> float:
        return self._limit_gb

    @staticmethod
    def from_dict(data: Dict):
        """
        :rtype: Usage
        """
        return Usage(
            id=data.get("id"),
            phone_number=data["phonenumber"],
            period_start=data["periodstart"],
            period_end=data["periodend"],
            created=data["created"],
            updated=data["updated"],
            used_gb=data["usedgb"],
            limit_gb=data["limitgb"],
            quota_name=data["quotaname"],
        )

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "phonenumber": self.phone_number,
            "periodstart": self.period_start,
            "periodend": self.period_end,
            "created": self.created,
            "updated": self.updated,
            "usedgb": self.used_gb,
            "limitgb": self.limit_gb,
            "quotaname": self.quota_name,
        }
