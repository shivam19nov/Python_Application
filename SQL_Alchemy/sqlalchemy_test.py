from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy import select
from sqlalchemy.engine.url import URL

def get_engine(conn_det):
    try:
        engine = create_engine(URL(**conn_det))
        return engine
        
    except Exception as err:
        print(err)

def get_conn(engine):
    try:
        conn = engine.connect()
        return conn
    except Exception as err:
        print(err)

def close_conn(conn):
    try:
        conn.close()
    except Exception as err:
        print(err)

def get_metadata(engine, schema_nm, table_nm):
    try:
        # Creating a metadata object for an schema
        metadata = MetaData(schema=schema_nm) 
        metadata.reflect(bind=engine)  
        # get SA Table object for a table
        table = metadata.tables[f'{schema_nm}.{table_nm}'] 
        return table
    except Exception as err:
        print(err)

if __name__ =='__main__':
    try : 
        # Postgres Connection Dictionary
        postgres_db = {'drivername': 'postgres',
                    'username': 'u_nm',
                    'password': 'pass',
                    'host': 'host.amazonaws.com',
                    'port': 5432,
                    'database': 'db_nm'
                    }

        pg_engine = get_engine(postgres_db)
        pg_conn = get_conn(pg_engine)
        pg_table = get_metadata(pg_engine, 'schema_nm', 'table_nm')

        # Get column list
        pg_col_list = pg_table.columns.keys()
        # Select 100 rows from table
        pg_select_st = select([pg_table]).limit(100)
        # execute the string
        pg_res = pg_conn.execute(pg_select_st)
        #print row as tuple
        for _row in pg_res:
            print(_row)
        
        # MYSQL Connection Dictionary
        mysql_db = {'drivername': 'mysql',
                    'username': 'u_nm',
                    'password': 'pass',
                    'host': 'host.amazonaws.com',
                    'port': 3306,
                    'database': 'db_nm'
                    }
        ms_engine = get_engine(mysql_db)
        ms_conn = get_conn(ms_engine)
        ms_table = get_metadata(ms_engine, 'schema_nm', 'table_nm')

        # Get column list
        ms_col_list = ms_table.columns.keys()
        # Select 100 rows from table
        ms_select_st = select([ms_table]).where(ms_table.c.col1 == '8080')
        # execute the string
        ms_res = ms_conn.execute(ms_select_st)
        #print row as tuple
        for _row in ms_res:
            print(_row)

    except Exception as err:
        print(err)

    finally:
        close_conn(pg_conn)
        close_conn(ms_conn)
