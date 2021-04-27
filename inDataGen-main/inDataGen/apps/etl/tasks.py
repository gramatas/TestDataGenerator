# Bonobo
import bonobo
import bonobo_sqlalchemy

# Bonobo utils
from apps.etl.bonobo_utils import SourceAPI, DestinationCSV, SourcePostgres, DestinationPostgres

# Bonobo Transformations
from apps.etl.bonobo_utils.transformations import Transformations


def run_graph(source_type, source_config, destination_type, destination_config, transformation_schema={}):
    """
    This task is in charge of creating and running a Bonobo graph
    :return:
    """
    services = {}

    if source_type == 'api':
        source = SourceAPI(**source_config)
        schema = source.get_schema()
    elif source_type == 'postgres':
        source_class = SourcePostgres(**source_config)

        # Validate connection and get schema
        source_class.check_connection()
        schema = source_class.get_schema()

        services['source_engine'] = source_class.engine
        source = source_class  # bonobo_sqlalchemy.Select(f'SELECT * FROM {source_config["table"]}', engine='source_engine')
    else:
        raise Exception("Source type not supported")

    if destination_type == 'csv':
        destination = DestinationCSV(**destination_config, schema=schema)
    elif destination_type == 'postgres':
        destination_class = DestinationPostgres(**destination_config, schema=schema)
        # Create table
        destination_class.check_connection()
        if not destination_class.check_table():
            destination_class.create_table()

        services['destination_engine'] = destination_class.engine
        destination = destination_class  # bonobo_sqlalchemy.InsertOrUpdate(destination_config["table"], engine='destination_engine')
    else:
        raise Exception("Destination type not supported")

    graph = bonobo.Graph(source, Transformations(transformation_schema), destination)

    bonobo.run(graph, services=services)

    if destination_type == 'csv':
        destination.file.close()

if __name__ == '__main__':
    """
    Test example
    """
    api_kwargs = {
        'url': 'https://rickandmortyapi.com/api/character',
        'pagination_param': 'page',
        'increase_by': 1,
        'starts_at': 1,
        'stop_at': 2,
        'list_path': 'results'
    }

    postgres_config = {
        'host': 'postgres',
        'dbname': 'etl',
        'port': 5432,
        'table': 'etl_datasource',
        'user': 'sBLRWyyPsInwHftmHAWmYJURGWBGFpYr',
        'pswd': 'tuXL3XSF8O7tsGrcGHoMos4tVNtL3tnrRshSCZokGnIfk4ArDyzaa297k2WgQPDV'
    }
    run_graph('postgres', postgres_config, 'csv', {'filename': 'test.csv'})

    # To test using django:
    # localhost:8000/test-etl?url=https%3A%2F%2Frickandmortyapi.com%2Fapi%2Fcharacter&pagination_param=page&increase_by=1&starts_at=1&stop_at=2&results_field=results
    # http://localhost:8000/test-etl/?url=https%3A//banks.data.fdic.gov/api/institutions%3Ffilters%3DSTALP%253AIA%2520AND%2520ACTIVE%253A1%26fields%3DZIP%252COFFDOM%252CCITY%252CCOUNTY%252CSTNAME%252CSTALP%252CNAME%252CACTIVE%252CCERT%252CCBSA%252CASSET%252CNETINC%252CDEP%252CDEPDOM%252CROE%252CROA%252CDATEUPDT%252COFFICES%26sort_by%3DOFFICES%26sort_order%3DDESC%26format%3Djson%26download%3Dfalse%26filename%3Ddata_file%26limit%3D50&pagination_param=offset&increase_by=10&starts_at=0&stop_at=20&list_path=data&object_path=data