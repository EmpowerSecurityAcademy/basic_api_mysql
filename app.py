from flask import Flask, url_for, request, jsonify
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
		cursor.execute("SELECT * from tasks")
		data = cursor.fetchone()
		return jsonify({'tasks': data})


	if request.method == 'POST':
		content = request.get_json(silent=True)
		cursor.execute("INSERT INTO tasks (title, description, done) VALUES('"+content['title'] +"', '"+ content['description'] +"', '"+ str(content['done']) + "')");
		conn.commit()
		return jsonify({'status_code': 201})

	return jsonify({'status_code': '400'})

# RESTFUL operations related to a specific task

@app.route('/todo/api/v1.0/tasks/<task_id>', methods=['GET', 'PUT', 'DELETE'])
def do_task(task_id):
	if request.method == 'GET':
		cursor.execute("SELECT * from tasks where id='" + task_id + "'")
		data = cursor.fetchone()
		return jsonify({'task': data})

	if request.method == 'PUT':
		content = request.get_json(silent=True)
		print("UPDATE tasks SET title='"+content['title'] +"', description='"+ content['description'] +"', done= '"+ str(content['done']) + "' where id='" + str(task_id))
		cursor.execute("UPDATE tasks SET title='"+content['title'] +"', description='"+ content['description'] +"', done= '"+ str(content['done']) + "' where id=" + str(task_id));
		conn.commit()
		return jsonify({'status_code': 200})

	if request.method == 'DELETE':
		cursor.execute("DELETE FROM tasks where id=" + str(task_id));
		conn.commit()
		return jsonify({'status_code': 200})

	return jsonify({'status_code': '400'})


if __name__ == '__main__':
    app.run(debug=True)