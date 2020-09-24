import epicbox
import asyncio

def sandbox_asm64(code, stdins=[""], callback=print):
    files = [{'name': 'main.asm', 'content': code.encode()}]
    compile_limits = {'cputime': 3, 'memory': 128}
    run_limits = {'cputime': 1, 'memory': 64}

    with epicbox.working_directory() as workdir:
        result = epicbox.run('asm64_compile', 'nasm -f elf64 -g main.asm', files=files, limits=compile_limits, workdir=workdir)
        result['type'] = 'compile'
        callback(result)

        if result["exit_code"] == 0:
            result = epicbox.run('asm64_compile', 'gcc -m64 -no-pie main.o -o main', files=files, limits=compile_limits, workdir=workdir)
            result['type'] = 'compile'
            callback(result)

            if result["exit_code"] == 0:
                for stdin in stdins:
                    result = epicbox.run('asm64_run', './main', files=files, limits=run_limits, workdir=workdir, stdin=stdin)
                    result['type'] = 'run'
                    callback(result)

def sandbox_cpp(code, stdins=[""], callback=print):
    files = [{'name': 'main.cpp', 'content': code.encode()}]
    compile_limits = {'cputime': 3, 'memory': 128}
    run_limits = {'cputime': 1, 'memory': 64}

    with epicbox.working_directory() as workdir:
        result = epicbox.run('gcc_compile', 'g++ -pipe -O2 -static -o main main.cpp', files=files, limits=compile_limits, workdir=workdir)
        result['type'] = 'compile'
        callback(result)

        if result["exit_code"] == 0:
            for stdin in stdins:
                result = epicbox.run('gcc_run', './main', files=files, limits=run_limits, workdir=workdir, stdin=stdin)
                result['type'] = 'run'
                callback(result)

def sandbox_c(code, stdins=[""], callback=print):
    files = [{'name': 'main.c', 'content': code.encode()}]
    compile_limits = {'cputime': 3, 'memory': 128}
    run_limits = {'cputime': 1, 'memory': 64}

    with epicbox.working_directory() as workdir:
        result = epicbox.run('gcc_compile', 'gcc main.c -o main', files=files, limits=compile_limits, workdir=workdir)
        result['type'] = 'compile'
        callback(result)

        if result["exit_code"] == 0:
            for stdin in stdins:
                result = epicbox.run('gcc_run', './main', files=files, limits=run_limits, workdir=workdir, stdin=stdin)
                result['type'] = 'run'
                callback(result)

def sandbox_csharp(code, stdins=[""], callback=print):
    files = [{'name': 'main.cs', 'content': code.encode()}]
    compile_limits = {'cputime': 3, 'memory': 128}
    run_limits = {'cputime': 1, 'memory': 64}

    with epicbox.working_directory() as workdir:
        result = epicbox.run('mono_compile', 'csc main.cs', files=files, limits=compile_limits, workdir=workdir)
        result['type'] = 'compile'
        callback(result)

        if result["exit_code"] == 0:
            for stdin in stdins:
                result = epicbox.run('mono_run', 'mono main.exe', files=files, limits=run_limits, workdir=workdir, stdin=stdin)
                result['type'] = 'run'
                callback(result)

def sandbox_java(code, stdins=[""], callback=print):
    files = [{'name': 'Main.java', 'content': code.encode()}]
    compile_limits = {'cputime': 5, 'memory': 128}
    run_limits = {'cputime': 1, 'memory': 64}

    with epicbox.working_directory() as workdir:
        result = epicbox.run('java_compile', 'javac Main.java', files=files, limits=compile_limits, workdir=workdir)
        result['type'] = 'compile'
        callback(result)

        if result["exit_code"] == 0:
            for stdin in stdins:
                result = epicbox.run('java_run', 'java Main', files=files, limits=run_limits, workdir=workdir, stdin=stdin)
                result['type'] = 'run'
                callback(result)

def sandbox_node(code, stdins=[""], callback=print):
    files = [{'name': 'index.js', 'content': code.encode()}]
    limits = {'cputime': 1, 'memory': 64}

    for stdin in stdins:
        result = epicbox.run('node_run', 'node index.js', files=files, limits=limits, stdin=stdin)
        result['type'] = 'run'
        callback(result)

def sandbox_python(code, stdins=[""], callback=print):
    files = [{'name': 'main.py', 'content': code.encode()}]
    limits = {'cputime': 1, 'memory': 64}

    for stdin in stdins:
        result = epicbox.run('python_run', 'python3 main.py', files=files, limits=limits, stdin=stdin)
        result['type'] = 'run'
        callback(result)

langs = {
    "python":   sandbox_python,
    "java":     sandbox_java,
    "node":     sandbox_node,
    "c":        sandbox_c,
    "c++":      sandbox_cpp,
    "c#":       sandbox_csharp,
    "asm64":    sandbox_asm64
}

epicbox.configure({
    'asm64_compile': {
        'docker_image': 'strellic/epicbox-asm64:latest',
        'user': 'root'
    },
    'asm64_run': {
        'docker_image': 'strellic/epicbox-asm64:latest',
        'user': 'sandbox',
    },

    'gcc_compile': {
        'docker_image': 'stepik/epicbox-gcc:6.3.0',
        'user': 'root'
    },
    'gcc_run': {
        'docker_image': 'stepik/epicbox-gcc:6.3.0',
        'user': 'sandbox',
    },

    'mono_compile': {
        'docker_image': 'stepik/epicbox-mono:5.0.0',
        'user': 'root'
    },
    'mono_run': {
        'docker_image': 'stepik/epicbox-mono:5.0.0',
        'user': 'sandbox',
    },

    'java_compile': {
        'docker_image': 'stepik/epicbox-java:11.0.1',
        'user': 'root'
    },
    'java_run': {
        'docker_image': 'stepik/epicbox-java:11.0.1',
        'user': 'sandbox',
    },

    'node_run': {
        'docker_image': 'stepik/epicbox-node:10.13.0',
        'user': 'sandbox',
    },

    'python_run': {
        'docker_image': 'strellic/epicbox-python:latest',
        'user': 'sandbox',
    }
})