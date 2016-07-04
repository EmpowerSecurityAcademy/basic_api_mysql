from flask import Flask, url_for, request, jsonify, make_response
from flask.ext.mysql import MySQL
from import_config import load_config
import json

config = load_config()

mysql = MySQL()
app = Flask(__name__)

app.config['MYSQL_DATABASE_USER'] = config["database"]["user_name"]
app.config['MYSQL_DATABASE_PASSWORD'] = config["database"]["password"]
app.config['MYSQL_DATABASE_DB'] = config["database"]["db_instance"]
app.config['MYSQL_DATABASE_HOST'] = config["database"]["connection_url"]

mysql.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()

url_root = '/todo/api/v3.0/'

@app.route(url_root+'tasks', methods=['GET', 'POST'])
def do_tasks():
	if request.method == 'GET':
		cursor.execute("SELECT * from tasks")
		data = cursor.fetchone()
		return make_response(jsonify({'tasks': data}), 200)


	if request.method == 'POST':
		content = request.get_json(silent=True)
		cursor.execute("INSERT INTO tasks (title, description, done) VALUES('"+content['title'] +"', '"+ content['description'] +"', '"+ str(content['done']) + "')");
		conn.commit()
		return make_response(jsonify({'inserted_id': cursor.lastrowid}), 201)

	return make_response(jsonify({'status_code': '400'}), 400)

# RESTFUL operations related to a specific task

@app.route(url_root+'tasks/<task_id>', methods=['GET', 'PUT', 'DELETE'])
def do_task(task_id):
	if request.method == 'GET':
		cursor.execute("SELECT * from tasks where id='" + task_id + "'")
		data = cursor.fetchone()
		if data != None:
			return make_response(jsonify({'task': data}), 200)
		else:
			return make_response(jsonify({'task': data}), 404)

	if request.method == 'PUT':
		content = request.get_json(silent=True)
		cursor.execute("UPDATE tasks SET title='"+content['title'] +"', description='"+ content['description'] +"', done= '"+ str(content['done']) + "' where id=" + str(task_id));
		conn.commit()
		cursor.execute("SELECT * from tasks where id='" + task_id + "'")
		data = cursor.fetchone()
		return make_response(jsonify({'task': data}), 200)

	if request.method == 'DELETE':
		cursor.execute("DELETE FROM tasks where id=" + str(task_id));
		conn.commit()
		return make_response(jsonify({'deleted_id': task_id}), 200)

	return make_response(jsonify({'status_code': '400'}), 400)


if __name__ == '__main__':
    app.run(debug=True)