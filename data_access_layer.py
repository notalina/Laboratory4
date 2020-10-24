import pymysql

class sql_translator:
    #db = pymysql.connect("localhost", "flask_user", "flask_user", "flask_user", port=3306)
    def select_sql(self, columns, table, condition):
        query = "SELECT "
        columns_names = ""
        if (len(columns) == 0):
            columns = "*"
        else:
            columns_names = ",".join(columns)
        return f"{query} {columns_names} FROM {table} WHERE {condition} ;"

    def delete_sql(self, database, condition):
        return f"DELETE FROM {database} WHERE {condition} ;"

    def insert_sql(self, table_name, columns, values):
        columns_names = ",".join(columns)
        values_str = ",".join(values)
        return f"INSERT {table_name}({columns_names}) VALUES ( {values_str} );"

    def update_sql(self, table_name: str, update_data: dict, where = "1=1"):
        update_str_list = [f"{column}={value}" for column, value in update_data.items()]
        update_expression = ", ".join(update_str_list)
        return f"UPDATE {table_name} SET {update_expression} WHERE {where};"
    
    def drop_sql(self, table):
        return f"DROP TABLE  {table};"
    
    def alter_execute(self, table, condition):
        return f"ALTER TABLE {table} {condition}"

    def create_sql(self, table_name: str, column_definitions: dict):
        update_str_list = [f"{column_name} {column_type}" for column_name,column_type in column_definitions.items()]
        update_expression = ", ".join(update_str_list)
        return f"CREATE TABLE {table_name} ({update_expression});"


    





