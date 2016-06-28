from flask import Flask, url_for, request
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

@app.route('/todo/api/v1.0/tasks', methods=['GET', 'POST', 'PUT'])
def do_tasks():
	if request.method == 'GET':
		return jsonify({'tasks': tasks})


	if request.method == 'POST':
		content = request.get_json(silent=True)
		tasks.append(content)
		return jsonify({'status_code': 201})

	#return proper status_code is object not found in tasks
	if request.method == 'PUT':
		content = request.get_json(silent=True)
		for x in tasks:
			if x['id'] == content['id']:
				x['title'] = content['title']
				x['description'] = content['description']
				x['done'] = content['done']
		return jsonify({'status_code': 200})

	return jsonify({'status_code': '400'})



# RESTFUL operations related to a specific task

@app.route('/todo/api/v1.0/tasks/<task_id>', methods=['GET', 'DELETE'])
def do_task(task_id):
	task_id = int(task_id)
	if request.method == 'GET':
		for task in tasks:
			if task['id'] == task_id:
				return jsonify(task)

	if request.method == 'DELETE':
		for task in tasks:
			if task['id'] == task_id:
				tasks.remove(task)
				return jsonify({'status_code': 200})

	return jsonify({'status_code': '400'})


if __name__ == '__main__':
    app.run(debug=True)