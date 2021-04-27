# SQLAlchemy
import sqlalchemy
from sqlalchemy.sql import select

# Utilities
from apps.etl.bonobo_utils.utils.postgres import Postgres


class SourcePostgres(Postgres):

    def get_first_row(self):
        """
        Verify connection to DB and return first row
        :return: First row
        """
        result = self.conn.execute(f'SELECT * FROM {self.table} LIMIT 1')
        for row in result:
            row = {col: row[i] for i, col in enumerate(self.schema.keys())}
            return row

    def __call__(self, *row, **kwargs):

        table = sqlalchemy.Table(
            self.table, self.metadata, extend_existing=True
        )

        s = select(table)
        result = self.conn.execute(s)

        for row in result:
            yield (dict(row._mapping), )
