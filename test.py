import data_access_layer

test = data_access_layer.dataAccessLayer()
test.select_execute(["id","name","age"], "people", "age > 5")
test.delete_execute("flask_user", "age > 5")
test.insert_execute("people", ["name","age"], ["алина","4"])
test.drop_execute("people")
