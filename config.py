import json

settings = {}
with open("data/settings.json", "r") as f:
    settings = json.loads(f.read())

bind = f"0.0.0.0:{settings['PORT']}"
worker_class = "eventlet"
workers = 1
