# Utilities
from apps.etl.bonobo_utils.utils.postgres import Postgres

# SQLAlchemy
import sqlalchemy

# Bonobo
from bonobo.constants import NOT_MODIFIED


class DestinationPostgres(Postgres):

    def create_table(self):
        """
        Create table in DB based on schema
        """

        # Get columns
        columns = []
        for i, (name, type_) in enumerate(self.schema.items()):
            if 'sqlalchemy' in str(type(type_)):
                pass
            else:
                type_ = str(type_).lower()

                if 'int' in type_:
                    type_ = sqlalchemy.Integer
                elif 'float' in type_:
                    type_ = sqlalchemy.Float
                elif 'bool' in type_:
                    type_ = sqlalchemy.Boolean
                elif 'timestamp' in type_:
                    type_ = sqlalchemy.TIMESTAMP
                elif 'varchar' in type_ or 'str' in type_:
                    type_ = sqlalchemy.VARCHAR
                elif 'json' in type_:
                    type_ = sqlalchemy.JSON
                elif 'datetime' in type_:
                    type_ = sqlalchemy.DateTime
                elif 'date' in type_:
                    type_ = sqlalchemy.Date
                else:
                    raise Exception(f"Column type {type_} not supported when creating a new table")

            columns.append(sqlalchemy.Column(name, type_))#, primary_key=True))

        columns = tuple(columns)
        table = sqlalchemy.Table(
            self.table, self.metadata,
            *columns
        )
        self.metadata.create_all(self.engine)

    def __call__(self, *row, **kwargs):

        row = row[0]
        columns = [f'"{c}"' for c in row.keys()]
        columns = ', '.join(columns)
        new_row = []
        for k, r in row.items():

            if 'json' in str(self.schema[k]).lower():
                new_row.append("'{}'".format(str(r).replace("'", '"')))
            if 'float' in str(self.schema[k]).lower() or 'in' in str(self.schema[k]).lower():
                new_row.append("{}".format(r))
            else:
                new_row.append("'{}'".format(str(r).replace("'", "''")))

        new_row = ', '.join(new_row)
        self.conn.execute(f"INSERT INTO {self.table} ({columns}) VALUES ({new_row})")

        return NOT_MODIFIED
