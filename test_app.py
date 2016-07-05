import os
import unittest
import app
from import_config import load_config
import json
from flask.ext.mysql import MySQL

mysql = MySQL()
config = load_config()

class AppTestCases(unittest.TestCase):

    def setUp(self):
        app.basic_api.config['MYSQL_DATABASE_USER'] = config["test_database"]["user_name"]
        app.basic_api.config['MYSQL_DATABASE_PASSWORD'] = config["test_database"]["password"]
        app.basic_api.config['MYSQL_DATABASE_DB'] = config["test_database"]["db_instance"]
        app.basic_api.config['MYSQL_DATABASE_HOST'] = config["test_database"]["connection_url"]
        self.app = app.basic_api.test_client()

    def test_get_tasks(self):
        response = self.app.get('/todo/api/v3.0/tasks')
        data = json.loads(response.data)
        self.assertEqual(data['tasks'], tasks)

    def test_post_tasks(self):
        response = self.app.post('/todo/api/v3.0/tasks', 
                       data=json.dumps(dict(title='Eat a sandwich', description='Enjoy it a lot', done=0)),
                       content_type = 'application/json')
        data = json.loads(response.data)
        self.assertEqual(data['id'], 3)

    # def test_get_task(self):
    #     response = self.app.get('/todo/api/v1.0/tasks/1')
    #     data = json.loads(response.data)
    #     self.assertEqual(data['task'], {
    #                                         'id': 1,
    #                                         'title': 'Buy groceries',
    #                                         'description': 'Milk, Cheese, Pizza, Fruit, Tylenol',
    #                                         'done': False
    #                                     })

    # def test_put_task(self):
    #     response = self.app.put('/todo/api/v1.0/tasks/1', 
    #                    data=json.dumps(dict(title='Order from Instacart', description='Milk, Cheese, Pizza, Fruit, Tylenol, Burrito', done=0)),
    #                    content_type = 'application/json')
    #     data = json.loads(response.data)
    #     self.assertEqual(data['task'], {
    #                                         'id': 1,
    #                                         'title': 'Order from Instacart',
    #                                         'description': 'Milk, Cheese, Pizza, Fruit, Tylenol, Burrito',
    #                                         'done': False
    #                                     })

    # def test_delete_task(self):
    #     self.app.post('/todo/api/v1.0/tasks', 
    #                    data=json.dumps(dict(title='Eat a sandwich', description='Enjoy it a lot', done=0)),
    #                    content_type = 'application/json')
    #     response = self.app.delete('/todo/api/v1.0/tasks/3')
    #     data = json.loads(response.data)
    #     self.assertEqual(data['deleted_id'], 3)

if __name__ == '__main__':
    unittest.main()