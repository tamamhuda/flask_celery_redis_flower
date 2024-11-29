
from flask import Flask
from flask import jsonify, request
from tasks import create_task, long_task, monitor_task
import json
dev_mode = True
app = Flask(__name__)


@app.route('/')
def index():
    return "Hello Flask, Redis, Celery, Flower from  Docker"

@app.post('/task-demo')
def run_task():
    content = request.json
    task_type = content["type"]
    task = create_task.delay(int(task_type))
    return jsonify({"task_id": task.id}), 202

# Route to trigger the task
@app.route('/start-task', methods=['POST'])
def start_task():
    data = {
        "arg1" : "...",
        "arg2" : "..."
    }
    task = long_task.apply_async(args=[data], retry=True, retry_policy={
    'max_retries': 3,
    'retry_errors': (TimeoutError, ),
})
    monitor_task.apply_async(args=[task.id])  # start monitor task
    return jsonify({
        'task_id': task.id,
        'status': 'Task started'
    }), 202

# Route to check task status
@app.route('/task-status/<task_id>', methods=['GET'])
def task_status(task_id):
    task = long_task.AsyncResult(task_id)
    
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'status': 'Task is pending...'
        }
    elif task.state == 'PROCESSING':
        response = {
            'state': task.state,
            'status': task.info.get('status', 'No status available')
        }
    elif task.state == 'SUCCESS':
        response = {
            'state': task.state,
            'status': task.info  # This is the return value from the task
        }
    elif task.state == 'FAILURE':
        response = {
            'state': task.state,
            'status': 'Task failed'
        }
    else:
        response = {
            'state': task.state,
            'status': 'Unknown state'
        }
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)