# CodeExec

CodeExec is a sandboxed coding platform for use in info-security Capture the Flag (CTF) competitions.
Initially created for GHCHS's CyberSecurity club, CodeExec was used in the club's two CTFs: BryceCTF and trevzCTF.

CodeExec uses the `epicbox` Python library to start one-use Docker containers to sandbox unsafe code.

Supports ASM64, C, C++, C#, Java 11, NodeJS 10.13.0, and Python 3.8.5.

Uses `socket.io` to communicate between a client and server.

## Installation

1. Install all of the necessary Docker images:

```bash
docker pull strellic/epicbox-asm64:latest && \
docker pull stepik/epicbox-gcc:6.3.0 && \
docker pull stepik/epicbox-mono:5.0.0 && \
docker pull stepik/epicbox-java:11.0.1 && \
docker pull stepik/epicbox-node:10.13.0 && \
docker pull strellic/epicbox-python:latest
```

2. Install the Python requirements with pip:

```bash
pip3 install -r requirements.txt
```

3. Run the app once to generate `settings.json` and `problems.json` in the `data` folder:

```bash
python3 app.py
````

4. Modify `settings.json` and `problems.json` to change the port and add challenges.

5. Set up the production server with gunicorn.

```bash
gunicorn -k gevent -w 1 -c config.py app:app
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)