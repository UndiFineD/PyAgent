# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_ovo.py\ovo.py\core.py\database.py\db_proxy_f6ed3ac14a26.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-ovo\ovo\core\database\db_proxy.py

from typing import Any, Self, Sequence

import pandas as pd

from sqlalchemy.orm.decl_api import DCTransformDeclarative


class DBProxy(DCTransformDeclarative):
    """Proxy class for DBEngine to enable db.Design.select() instead of db.select(Design)

    It provides a subset of methods of DBEngine (methods that operate on a single model class).

    """

    def _db(self):
        from ovo import db

        return db

    def remove(cls, *id_args, **kwargs):
        return cls._db().remove(cls, *id_args, **kwargs)

    def save_value(cls, column: str, value, **kwargs):
        return cls._db().save_value(cls, column, value, **kwargs)

    def select(cls, limit: int = None, order_by=None, **kwargs) -> Sequence[Self]:
        return cls._db().select(cls, limit=limit, order_by=order_by, **kwargs)

    def count(cls, **kwargs) -> int:
        return cls._db().count(cls, **kwargs)

    def count_distinct(cls, field="id", group_by=None, **kwargs) -> int | dict[Any, int]:
        return cls._db().count_distinct(cls, field=field, group_by=group_by, **kwargs)

    def get(cls, *id_args, **kwargs) -> Self:
        return cls._db().get(cls, *id_args, **kwargs)

    def get_value(cls, column: str, *id_args, raw=False, **kwargs):
        return cls._db().get_value(cls, column, *id_args, raw=raw, **kwargs)

    def select_values(cls, column: str, order_by=None, **kwargs) -> list:
        return cls._db().select_values(cls, column, order_by=order_by, **kwargs)

    def select_dict(cls, key_column: str, value_column: str, order_by=None, **kwargs) -> dict:
        return cls._db().select_dict(cls, key_column, value_column, order_by=order_by, **kwargs)

    def select_unique_values(cls, column: str, **kwargs) -> set:
        return cls._db().select_unique_values(cls, column, **kwargs)

    def select_dataframe(cls, index_col: str = "id", order_by=None, limit=None, **kwargs) -> pd.DataFrame:
        return cls._db().select_dataframe(cls, index_col=index_col, order_by=order_by, limit=limit, **kwargs)
