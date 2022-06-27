gunicorn queue_app:app -—daemon
python worker.py 
