from flask import Flask, url_for, request, jsonify, make_response, g
from flask.ext.mysql import MySQL
from import_config import load_config
import json
import types

config = load_config()

mysql = MySQL()
basic_api = Flask(__name__)

basic_api.config['MYSQL_DATABASE_USER'] = config["database"]["user_name"]
basic_api.config['MYSQL_DATABASE_PASSWORD'] = config["database"]["password"]
basic_api.config['MYSQL_DATABASE_DB'] = config["database"]["db_instance"]
basic_api.config['MYSQL_DATABASE_HOST'] = config["database"]["connection_url"]

mysql.init_app(basic_api)

url_root = '/todo/api/v3.0/'

def format_json(element):
	new_task = {}
	new_task["id"] = element[0]
	new_task["title"] = element[1]
	new_task["description"] = element[2]
	new_task["done"] = element[3]
	return new_task

@basic_api.before_request
def db_connect():
	g.db_conn = mysql.connect()

@basic_api.teardown_request
def db_disconnect(exception=None):
	g.db_conn.close()


@basic_api.route(url_root+'tasks', methods=['GET', 'POST'])
def do_tasks():
	cursor = g.db_conn.cursor()
	if request.method == 'GET':
		cursor.execute("SELECT * from tasks")
		data = cursor.fetchall()
		data_response = []
		for element in data:
			task = format_json(element)
			data_response.append(task)
		return make_response(jsonify({'tasks': data_response}), 200)

	if request.method == 'POST':
		content = request.get_json(silent=True)
		cursor.execute("INSERT INTO tasks (title, description, done) VALUES('"+content['title'] +"', '"+ content['description'] +"', '"+ str(content['done']) + "')");
		g.db_conn.commit()
		return make_response(jsonify({'id': cursor.lastrowid}), 201)

	return make_response(jsonify({'status_code': '500'}), 500)

# RESTFUL operations related to a specific task

@basic_api.route(url_root+'tasks/<task_id>', methods=['GET', 'PUT', 'DELETE'])
def do_task(task_id):
	cursor = g.db_conn.cursor()
	if request.method == 'GET':
		cursor.execute("SELECT * from tasks where id='" + task_id + "'")
		data = cursor.fetchone()
		if data != None:
			return make_response(jsonify({'task': format_json(data)}), 200)
		else:
			return make_response(jsonify({'task': data}), 404)

	if request.method == 'PUT':
		content = request.get_json(silent=True)
		cursor.execute("UPDATE tasks SET title='"+content['title'] +"', description='"+ content['description'] +"', done= '"+ str(content['done']) + "' where id=" + str(task_id));
		g.db_conn.commit()
		cursor.execute("SELECT * from tasks where id='" + task_id + "'")
		data = cursor.fetchone()
		return make_response(jsonify({'task': format_json(data)}), 200)

	if request.method == 'DELETE':
		cursor.execute("DELETE FROM tasks where id=" + str(task_id));
		g.db_conn.commit()
		return make_response(jsonify({'deleted_id': task_id}), 200)

	return make_response(jsonify({'status_code': '500'}), 500)

if __name__ == '__main__':
    basic_api.run(debug=True, host='0.0.0.0', port=5003)