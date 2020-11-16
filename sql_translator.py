class SqlTranslator:
    def select_sql(self,db_name, table, columns=[], condition="1=1"):
        query = "SELECT"
        columns_names = ""
        #тоже самое и в других запросах надо сделать
        if db_name:
            table = f"{db_name}.{table}"
        if (len(columns) == 0):
            columns_names = "*"
        else:
            columns_names = ",".join(columns)
        return f"{query} {columns_names} FROM {table} WHERE {condition};"

    def delete_sql(self, db_name, database, condition="1=1"):
        if db_name:
            table = f"{db_name}.{table}"
        return f"DELETE FROM {database} WHERE {condition};"

    def insert_sql(self, db_name, table_name, columns, values):
        if db_name:
            table = f"{db_name}.{table}"
        columns_names = ",".join(columns)
        values_str = ",".join(values)
        return f"INSERT INTO {table_name}({columns_names}) VALUES ( {values_str} );"

    def update_sql(self, db_name, table_name: str, update_data: dict, where = "1=1"):
        if db_name:
            table = f"{db_name}.{table}"
        update_str_list = [f"{column}={value}" for column, value in update_data.items()]
        update_expression = ", ".join(update_str_list)
        return f"UPDATE {table_name} SET {update_expression} WHERE {where};"
    
    def drop_sql(self, db_name, table):
        if db_name:
            table = f"{db_name}.{table}"
        return f"DROP TABLE {table};"
    
    def alter_sql(self, db_name, table, condition):
        if db_name:
            table = f"{db_name}.{table}"
        return f"ALTER TABLE {table} {condition};"

    def create_sql(self, db_name, table_name: str, column_definitions: dict):
        if db_name:
            table = f"{db_name}.{table}"
        update_str_list = [f"{column_name} {column_type}" for column_name,column_type in column_definitions.items()]
        update_expression = ", ".join(update_str_list)
        return f"CREATE TABLE {table_name} ({update_expression});"

    def create_database_sql(self, db_name):
        return f"CREATE DATABASE {db_name};"

    def drop_database_sql(self, db_name):
        return f"DROP DATABASE {db_name};"
    





