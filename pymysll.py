import yaml
import pymysql
import pandas as pd
db_yml = yaml.safe_load(open('db.yaml'))
# initiate a connection
def initiate_con():
    try:
        connection = pymysql.connect(
            host=db_yml['mysql_host'],
            user=db_yml['mysql_user'],
            password=db_yml['mysql_password'],
            db = db_yml['mysql_db'],
            #CURSORCLASS=pymysql.cursors.DictCursor
        )
        print("Connection sucessfull")
    except Exception as e:
        print(e)
        connection = None
    return connection
# we are calling initiate_con() to establish connection so that we can now acess the data base
connection =initiate_con()
# now connecion has been created we need to run queries
# we need cursor for this
# execute() is used to execute the query
query = (f'select * from visitor;')
def get_records(query):
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
        # results need to be commit
        connection.commit()
        # fetch all the records from SQL query output
        results = cursor.fetchall()
        # convert into pandas dataframe
        df = pd.DataFrame(results)
        print(f'Sucessfully retrievd records')
        return df
    except:
        print(f'error occured')
df = get_records(query)
print(df.head())