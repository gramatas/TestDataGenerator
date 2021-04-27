# SQLAlchemy
import sqlalchemy


class Postgres:
    """
    PostgreSQL Class to validate DB and get table schema
    """
    def __init__(self, host, dbname, port, table, user, pswd, schema={}):
        """
        Initialize connection to Postgres DB
        :param host: DB Host
        :param dbname: DB Name
        :param port: DB Port
        :param table: DB Table
        :param user: DB User
        :param pswd: DB Password
        """

        self.table = table
        self.engine = sqlalchemy.create_engine(f"postgresql+psycopg2://{user}:{pswd}@{host}:{port}/{dbname}")
        self.conn = None
        self.schema = schema

    def check_connection(self):
        """Verify if it is possible to stablish a connection"""
        try:
            self.conn = self.engine.connect()
        except:
            return False
        else:
            self.metadata = sqlalchemy.MetaData(bind=self.engine)
            self.metadata.reflect()
            return True

    def check_table(self):
        """Verify if the table already exists"""
        try:
            self.metadata.tables[self.table]
        except KeyError:
            return False
        else:
            return self.get_schema()

    def get_schema(self, force=False):
        """
        Get schema from table
        """
        if not self.schema or force:
            for c in self.metadata.tables[self.table].columns:
                self.schema[c.name] = c.type

        return self.schema


if __name__ == '__main__':
    source = Postgres('postgres', 'etl', 5432, 'etl_datasource', 'sBLRWyyPsInwHftmHAWmYJURGWBGFpYr',
                   'tuXL3XSF8O7tsGrcGHoMos4tVNtL3tnrRshSCZokGnIfk4ArDyzaa297k2WgQPDV')

    source.get_schema()
    print(source.schema)
    print(source.get_first_row())