import os
import time
from celery import Celery


celery = Celery('tasks', 
                broker=os.environ["CELERY_BROKER_URL"], 
                backend=os.environ["CELERY_RESULT_BACKEND"])


@celery.task(name="create_task")
def create_task(task_type):
    time.sleep(int(task_type) * 2)
    return True

@celery.task(bind=True, name="Long Task")
def long_task(self, data):
    """Simulate a long-running task."""
    # Mark task as processing
    self.update_state(state='PROCESSING', meta={'status': 'Task is being processed'})
    
    # Simulate work (replace with actual processing logic)
    for i in range(10):
        time.sleep(1)  # Simulating work

    # Task completed successfully
    return data

@celery.task(bind=True, name="Monitor Task")
def monitor_task(self, task_id):
    """
    Task ini digunakan untuk memonitor status task utama.
    Ini akan memeriksa status task utama secara berkala.
    """
    while True:
        task = long_task.AsyncResult(task_id)
        if task.state == 'PENDING':
            # Jika task masih pending
            self.update_state(state='PROGRESS', meta={'status': 'Task is pending...'})
            print({"state" : task.state})
        elif task.state == 'PROCESSING':
            # Jika task sedang dalam progress
            current = task.info.get('current', 0)
            total = task.info.get('total', 1)
            status = task.info.get('status', 'No status available')
            self.update_state(state='PROGRESS', meta={'status': f'{status} - {current}/{total}'})
            print({"state" : task.state})
        elif task.state == 'SUCCESS':
            # Jika task sudah selesai
            self.update_state(state='SUCCESS', meta={'status': 'Task completed successfully!'})
            print({"state" : task.state})
            break
        elif task.state == 'FAILURE':
            # Jika task gagal
            self.update_state(state='FAILURE', meta={'status': 'Task failed'})
            print({"state" : task.state})
            break
        else:
            # Jika state tidak dikenali
            self.update_state(state='UNKNOWN', meta={'status': 'Unknown state'})
        
        time.sleep(1)  # Cek status setiap 2 detik
