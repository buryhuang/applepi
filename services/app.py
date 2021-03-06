#!/usr/bin/python
from flask import Flask, jsonify, url_for, request
import json
from pprint import pprint
import subprocess
import os

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

@app.route('/transpo/api/v1.0/hts/<string:hts_id>', methods = ['GET'])
def get_hts(hts_id):
    response = {}
    results = []
    hts_id = hts_id.replace('.', '')
    #response['result'] = [{'htsno' : hts_id, 'description' : 'tmp'}]
    for line in htsdata:
        if line['htsno'].replace('.','').startswith(hts_id):
            results.append({'htsno' : line['htsno'], 'description' : line['description']})
    if len(results) == 0:
        results = [{'htsno' : hts_id, 'description' : 'NOT FOUND'}]
    response['result'] = results
    return jsonify(response)

@app.route('/transpo/api/v1.0/shipment/create', methods = ['POST'])
def shipment_create():
    # format: "shipment_id": "000001"
    body = request.get_json()
    if "shipment_id" not in body or len(body['shipment_id'].lstrip().rstrip()) == 0:
        return jsonify({'error' : 'Mendatory fields not present: shipment_id'}), 400
    shipment_id = body['shipment_id'].lstrip().rstrip()
    with open('shipments/%s.json' % shipment_id,'w') as outfile:
        json.dump(body, outfile)
    return jsonify(body), 201

@app.route('/transpo/api/v1.0/shipment/query/<string:shipment_id>', methods = ['GET'])
def shipment_query(shipment_id):
    # format: "shipment_id": "000001"
    shipment_id = shipment_id.lstrip().rstrip()
    if len(shipment_id) == 0:
        return jsonify({'error' : 'Mendatory fields is empty: shipment_id'}), 404
    file_path = 'shipments/%s.json' % shipment_id
    if not os.path.exists(file_path):
        return jsonify({'error' : 'Cannot find record: %s' % shipment_id}), 404
    body = {}
    with open(file_path, 'r') as infile:
        body = json.load(infile)
    response_body = {'status' : 'CREATED', 'shipment' : body}
    return jsonify(response_body)

@app.route('/transpo/api/v1.0/shipment/list', methods=['GET'])
def shipment_list():
    files = next(os.walk('shipments/'))[2]
    return jsonify({'shipments': files})

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
