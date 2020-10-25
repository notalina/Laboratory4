

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

def test_sql_select_tranlator_1():
    sql = sql_translator.SqlTranslator()
    actual = sql.select_sql("table1")
    expected = "SELECT * FROM table1 WHERE 1=1;"
    assert actual == expected

def test_delete_translator():
    sql = sql_translator.SqlTranslator()
    actual = sql.delete_sql("table1", "id > 10")
    expected = "DELETE FROM table1 WHERE id > 10;"
    assert actual == expected

def test_delete_translator_1():
    sql = sql_translator.SqlTranslator()
    actual = sql.delete_sql("table1")
    expected = "DELETE FROM table1 WHERE 1=1;"
    assert actual == expected

def test_insert_translator():
    sql = sql_translator.SqlTranslator()
    actual = sql.insert_sql("table1",["column1","column2"],["alina", "kasimova"])
    expected = "INSERT INTO table1(column1,column2) VALUES ( alina,kasimova );"
    assert actual == expected

def test_update_translator():
    sql = sql_translator.SqlTranslator()
    updated_data = {"column1":1, "column2": 2}
    actual = sql.update_sql("table1", updated_data)
    expected = "UPDATE table1 SET column1=1, column2=2 WHERE 1=1;"
    assert actual == expected

def test_update_translator_1():
    sql = sql_translator.SqlTranslator()
    updated_data = {"column1":1, "column2": 2}
    actual = sql.update_sql("table1", updated_data, "column1=0")
    expected = "UPDATE table1 SET column1=1, column2=2 WHERE column1=0;"
    assert actual == expected

def test_drop_translator():
    sql = sql_translator.SqlTranslator()
    actual = sql.drop_sql("table1")
    expected = "DROP TABLE table1;"
    assert actual == expected

def test_alter_translator():
    sql = sql_translator.SqlTranslator()
    actual = sql.alter_sql("table1", "DROP COLUMN column1")
    expected = "ALTER TABLE table1 DROP COLUMN column1;"
    assert actual == expected

def test_create_translator():
    sql = sql_translator.SqlTranslator()
    column_definitions = {"column1":"INTEGER", "column2": "STRING"}
    actual = sql.create_sql("table1", column_definitions)
    expected = "CREATE TABLE table1 (column1 INTEGER, column2 STRING);"
    assert actual == expected

def test_mysql_db_select():
    dal = data_access_layer.DataAccessLayer("localhost", 3306, "flask_user", "flask_user", "flask_user")
    results = dal.select("SELECT * FROM persons;")
    assert len(results) > 0

if __name__ == "__main__":
    test_create_translator()