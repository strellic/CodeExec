# CodeExec

CodeExec is a sandboxed coding platform for use in info-security Capture the Flag (CTF) competitions.
Initially created for GHCHS's CyberSecurity club, CodeExec was used in the club's two CTFs: BryceCTF and trevzCTF.

CodeExec uses the `epicbox` Python library to start one-use Docker containers to sandbox unsafe code.

Supports ASM64, C, C++, C#, Java 11, NodeJS 10.13.0, and Python 3.8.5.

Uses `socket.io` to communicate between a client and server.

## Screenshots
![](https://i.gyazo.com/8eec9fd6ff130af5354244919e7ae755.png)
![](https://i.gyazo.com/998927315e68e733491ad3469751feb4.png)

## Installation

1. Install all of the necessary Docker images:

```bash
docker pull strellic/epicbox-asm64:latest && \
docker pull stepik/epicbox-gcc:6.3.0 && \
docker pull stepik/epicbox-mono:5.0.0 && \
docker pull stepik/epicbox-java:11.0.1 && \
docker pull strellic/epicbox-node:latest && \
docker pull strellic/epicbox-python:latest
```

(OPTIONAL) Use `venv` to make a virtual environment:

```bash
python3 -m venv env
source env/bin/activate
```

2. Install the Python requirements with pip:

```bash
pip install -r requirements.txt
```

3. Run the app once in Flask debug mode to generate `settings.json` and `problems.json` in the `data` folder:

```bash
python3 app.py
````

4. Modify `settings.json` and `problems.json` to change the port and add challenges.

5. When you want to switch from Flask to a production server, start the app with Gunicorn.

```bash
gunicorn -k eventlet -w 1 -c config.py app:app
```

(If at this point, `gunicorn` doesn't work, install `gunicorn` or `gunicorn3` from your package manager and run the previous command again.)

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)
