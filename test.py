

import sql_translator
import data_access_layer

# if __name__ == "__main__":
#     dal = data_access_layer.DataAccessLayer("вот","тут","подключаемся","к","БД")
#     # для теста можно и тут вызывать SqlTranslator
#     sql = sql_translator.SqlTranslator()
#     sql.select_sql("реальная таблица", [])

def test_sql_select_tranlator():
    sql = sql_translator.SqlTranslator()
    actual = sql.select_sql("table", ["col1", "col2"], "id=1")
    expected = "SELECT col1,col2 FROM table WHERE id=1;"
    assert actual == expected


def test_mysql_db_select():
    dal = data_access_layer.DataAccessLayer("localhost", 3306, "flask_user", "flask_user", "flask_user")
    results = dal.select("тут типа селект с реальной таблицы с реальными данными")
    assert len(results) > 0

if __name__ == "__main__":
    test_sql_select_tranlator()





