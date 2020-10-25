import pymysql 

class DataAccessLayer:
    def __init__(self, db_host, dp_port, db_name, db_user, db_user_password):
        self.db_host = db_host
        self.dp_port = dp_port
        self.db_name = db_name
        self.db_user = db_user
        self.db_user_password = db_user_password
        
    def get_connection(self):
        try: 
            connection = pymysql.connect(host=self.db_host, 
                                        port=self.dp_port,
                                        database=self.db_name, 
                                        user=self.db_user,
                                        password=self.db_user_password)    
            connection.autocommit(True)     
        except pymysql.MySQLError as e:
            print("Error while connecting to MySQL", e)
            raise
        return connection

    #DML

    def select(self, select_query: str):
        try:
            connection = self.get_connection()
            with connection.cursor() as cursor:
                cursor.execute(select_query)
                results = cursor.fetchall()
                return results
        except pymysql.MySQLError as e:
            print(f"Error execute select query {select_query} to MySQL", e)
            raise
        finally:
            connection.close()
    
    def update(self, update_query: str):
        try:
            connection = self.get_connection()
            with connection.cursor() as cursor:
                cursor.execute(update_query)
        except pymysql.MySQLError as e:
            print(f"Error execute update query {update_query} to MySQL", e)
            raise
        finally:
            connection.close()

    def delete(self, delete_query: str):
        try:
            connection = self.get_connection()
            with connection.cursor() as cursor:
                cursor.execute(delete_query)
        except pymysql.MySQLError as e:
            print(f"Error execute delete query {delete_query} to MySQL", e)
            raise
        finally:
            connection.close()

    def insert(self, insert_query: str):
        try:
            connection = self.get_connection()
            with connection.cursor() as cursor:
                cursor.execute(insert_query)
        except pymysql.MySQLError as e:
            print(f"Error execute insert query {insert_query} to MySQL", e)
            raise
        finally:
            connection.close()
    
    #DDL

    def create(self, create_query: str):
        try:
            connection = self.get_connection()
            with connection.cursor() as cursor:
                cursor.execute(create_query)
        except pymysql.MySQLError as e:
            print(f"Error execute create query {create_query} to MySQL", e)
            raise
        finally:
            connection.close()

    def alter(self, alter_query: str):
        try:
            connection = self.get_connection()
            with connection.cursor() as cursor:
                cursor.execute(alter_query)
        except pymysql.MySQLError as e:
            print(f"Error execute alter query {alter_query} to MySQL", e)
            raise
        finally:
            connection.close()

    def drop(self, drop_query: str):
        try:
            connection = self.get_connection()
            with connection.cursor() as cursor:
                cursor.execute(drop_query)
        except pymysql.MySQLError as e:
            print(f"Error execute drop query {drop_query} to MySQL", e)
            raise
        finally:
            connection.close()

    

    

"""
 Идя вообще такаая
у тебя есть типа 3 слоя это контроллер которые описаны в app.py 
они принимают запросы и принимают решения что с этим делать
есть "вьюхи" это наши шаблоны они принимают в себя входные данные 
и отрисовывают себя клиенту то бишь браузеру
и есть "модели" у нас это типа слой работы с бд
.по скольку у нас нет чистых моделей  мы делаем чутка иначе
у нас логика такая как мне кажется

контроллер принимает запрос -> парсит его входные данные -> если они ок -> генерирует запрос ->
полученный запрос сохраняет пока в переемеенную -> передает запрос в DataAccessLayer -> результат запроса тоже типа сохраняете в переменную ->
переменные отправляются в шаблон и рендеерятся клиенту


"""
#хорошо, понятно
