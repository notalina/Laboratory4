import pymysql

class dataAccessLayer:
    #db = pymysql.connect("localhost", "flask_user", "flask_user", "flask_user", port=3306)
    def select_execute(self, columns, table, condition):
        query = "SELECT "
        columns_names = ""
        if (len(columns) == 0):
            columns = "*"
        else:
            columns_names = ",".join(columns)
        query = f"{query} {columns_names} FROM {table} WHERE {condition} ;"
        print(query)

    def delete_execute(self, database, condition):
        query = f"DELETE FROM {database} WHERE {condition} ;"
        print(query)

    def insert_execute(self, table_name, columns, values):
        columns_names = ",".join(columns)
        values_str = ",".join(values)
        query = f"INSERT {table_name}({columns_names}) VALUES ( {values_str} );"
        print(query)

    def update()
    
    def drop_execute(self, table):
        query = f"DROP TABLE  {table};"
        print(query)
    
    def alter_execute(self, table, ):

    def create_execute(self, ):


    





