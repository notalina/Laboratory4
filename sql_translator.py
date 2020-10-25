class SqlTranslator:
    def select_sql(self, table, columns=[], condition="1=1"):
        query = "SELECT"
        columns_names = ""
        if (len(columns) == 0):
            columns_names = "*"
        else:
            columns_names = ",".join(columns)
        return f"{query} {columns_names} FROM {table} WHERE {condition};"

    def delete_sql(self, database, condition="1=1"):
        return f"DELETE FROM {database} WHERE {condition};"

    def insert_sql(self, table_name, columns, values):
        columns_names = ",".join(columns)
        values_str = ",".join(values)
        return f"INSERT INTO {table_name}({columns_names}) VALUES ( {values_str} );"

    def update_sql(self, table_name: str, update_data: dict, where = "1=1"):
        update_str_list = [f"{column}={value}" for column, value in update_data.items()]
        update_expression = ", ".join(update_str_list)
        return f"UPDATE {table_name} SET {update_expression} WHERE {where};"
    
    def drop_sql(self, table):
        return f"DROP TABLE {table};"
    
    def alter_sql(self, table, condition):
        return f"ALTER TABLE {table} {condition};"

    def create_sql(self, table_name: str, column_definitions: dict):
        update_str_list = [f"{column_name} {column_type}" for column_name,column_type in column_definitions.items()]
        update_expression = ", ".join(update_str_list)
        return f"CREATE TABLE {table_name} ({update_expression});"


    





