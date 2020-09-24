from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from colorama import Fore, Style
import json

import sandbox
import utils

settings, problems = utils.load_data()

app = Flask("codeexec",
    static_url_path='', 
    static_folder='static'
)

sio = SocketIO(app)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@sio.on('connect')
def connect():
    emit('problems', [p['name'] for p in problems])

@sio.on('run')
def run(data):
    code = data['code']
    lang = data['lang']
    stdin = data['stdin']
    problem = data['problem']

    if not code or not lang:
        return emit('err', '[ERROR] No code or language submitted!')

    if lang not in sandbox.langs.keys():
        return emit('err', '[ERROR] Invalid language.')

    if problem:
        problem = [p for p in problems if p['name'] == problem][0]
        if not problem:
            return emit('err', '[ERROR] Invalid task.')

    executor = sandbox.langs[lang]
    
    if not problem:
        executor(code, [stdin], outputHandler)
    else:
        test_cases = [p['stdin'] for p in problem['tests']]
        test_check = [p['stdout'] for p in problem['tests']]

        passed = True
        failed = 0
        i = 0

        def check(result):
            nonlocal passed
            nonlocal failed
            nonlocal i

            if utils.check_testcase(result['stdout'].decode(), test_check[i]):
                emit('out', f'{Fore.WHITE}[Task] Passed test case {i + 1} / {len(test_cases)}.\n')
            else:
                emit('err', f'{Fore.RED}[Task] Failed test case {i + 1} / {len(test_cases)}.\n')
                failed += 1
                passed = False

            i += 1

            if i == len(test_cases):
                end()

        def end():
            if passed:
                emit('out', f"{Fore.BLUE}\nNice job! You passed the task. Here's your flag:\n{Style.BRIGHT}{problem['flag']}")
            else:
                emit('err', f"{Fore.RED}\nTask {Style.BRIGHT}{problem['name']}{Style.NORMAL} failed.\n{failed} / {len(test_cases)} test cases failed.")

        executor(code, test_cases, check)


def outputHandler(result):
    if result['stderr']:
        if result['type'] == 'compile':
            emit('err', f'{Fore.RED}[ERROR] There was an error compiling your code.\n\n')
        else:
            emit('err', f'{Fore.RED}[ERROR] There was an error running your code.\n\n')
        emit('err', f"{Fore.RED}{result['stderr'].decode()}")

    if result['type'] == 'compile':
        return

    emit('out', f"{Fore.WHITE}{result['stdout'].decode()}")

    if result['exit_code'] == 0:
        emit('out', f"{Fore.WHITE}\n-------------------------\n\nThe program executed successfully.\nDuration: {result['duration']}s\n\n\n")
    else:
        emit('err', f"{Fore.RED}\n-------------------------\n\nThe program failed to run.\nDuration: {result['duration']}s\nTimeout: {result['timeout']}\nOut of Memory: {result['oom_killed']}\n\n\n")

if __name__ == '__main__':
    sio.run(app, host='0.0.0.0', port=settings['PORT'])