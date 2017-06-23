#!/usr/bin/python
from flask import Flask, jsonify, url_for
import json
from pprint import pprint
import subprocess

htsdata = []

app = Flask(__name__)

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]

def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id = task['id'], _external = True)
        else:
            new_task[field] = task[field]
    return new_task

@app.route('/applepi/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

@app.route('/applepi/api/v1.0/tasks/<string:task_id>', methods = ['GET'])
def get_task(task_id):
    #task = filter(lambda t: t['id'] == task_id, tasks)
    #if len(task) == 0:
    #    abort(404)
    #return jsonify( { 'task': make_public_task(task[0]) } )
    response = 'Not executed'
    if task_id == 'poweroff':
        response = 'Powering off in 1 minute'
        response += subprocess.check_output("shutdown -P +1", shell=True)
    elif task_id == 'list':
        response = subprocess.check_output("ls -l", shell=True)
    return jsonify({'task' : task_id, 'status' : 0, 'message' : response})

@app.route('/applepi/api/v1.0/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': task}), 201

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response

if __name__ == '__main__':
    print 'Loading HTS database'
    with open('htsdata2017.json') as data_file:
        htsdata = json.load(data_file)

    print 'Starting web server'
    app.run(debug=True, host='0.0.0.0', port=80)
