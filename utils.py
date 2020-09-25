import json
import os
import re

def load_data():
	settings = {}
	problems = []

	if not os.path.isdir("data"):
		os.makedirs("data")

	if not os.path.exists("data/settings.json"):
		settings = {
			"PORT": 8010 # DEFAULT PORT
		}
		with open("data/settings.json", "w") as f:
			f.write(json.dumps(settings, indent=4))
	else:
		with open("data/settings.json", "r") as f:
			settings = json.loads(f.read())

	if not os.path.exists("data/problems.json"):
		problems = [
			{
				"name": "Hello World!",
				"tests": [
					{"stdin": "", "stdout": "Hello World!"},
					{"stdin": "nice!", "stdout": "Hello World!"},
				],
				"flag": "flag{example_problem}"
			}
		]
		with open("data/problems.json", "w") as f:
			f.write(json.dumps(problems, indent=4))
	else:
		with open("data/problems.json", "r") as f:
			problems = json.loads(f.read())

	with open("data/settings.json", "w") as f:
		f.write(json.dumps(settings, indent=4))
	with open("data/problems.json", "w") as f:
		f.write(json.dumps(problems, indent=4))

	return settings, problems

def check_testcase(output, answer):
	trimmer = r'^\s+|\s+$'
	return output == answer or re.sub(trimmer, '', output) == re.sub(trimmer, '', answer)