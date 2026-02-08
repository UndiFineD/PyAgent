# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\agno.py\libs.py\agno.py\agno.py\vectordb.py\cassandra.py\extra_param_mixin_1cc6f732dfcd.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\agno\libs\agno\agno\vectordb\cassandra\extra_param_mixin.py

from typing import List

from cassio.table.mixins.base_table import BaseTableMixin

from cassio.table.table_types import ColumnSpecType

class ExtraParamMixin(BaseTableMixin):

    def _schema_da(self) -> List[ColumnSpecType]:

        return super()._schema_da() + [

            ("document_name", "TEXT"),

        ]

