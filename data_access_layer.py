import pymysql

class dataAccessLayer:
    #db = pymysql.connect("localhost", "flask_user", "flask_user", "flask_user", port=3306)
    def select_execute(self, columns, table, condition):
        query = "SELECT "
        columns_names = ""
        if (len(columns) == 0):
            columns = "*"
        else:
            for i in range(len(columns)):
                if (i!= len(columns)-1):
                    columns_names += columns[i]
                    columns_names += ', '
                else:
                    columns_names += columns[i]
        query = query + columns_names + " FROM " + table + " WHERE " + condition + ';'
        print(query)

    def delete_execute(self, database, condition):
        query = "DELETE FROM " + database + " WHERE " + condition + ';'
        print(query)

    def insert_execute(self, table_name, columns, values):
        columns_names = ""
        values_str = ""
        for i in range(len(columns)):
            if (i!= len(columns)-1):
                columns_names += columns[i]
                columns_names += ', '
            else:
                columns_names += columns[i]
        for i in range(len(values)):
            if (i!= len(values)-1):
                values_str += values[i]
                values_str += ', '
            else:
                values_str += values[i]
        query = "INSERT " + table_name + '(' + columns_names + ')' + " VALUES " + "(" + values_str + ")" + ';'
        print(query)
    
    def drop_execute(self, table):
        query = "DROP TABLE " + table + ';'
        print(query)
    
    def alter_execute(self, table, ):

    





