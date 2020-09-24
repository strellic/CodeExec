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
`pip3 install -r requirements.txt`

3. Run the app once to generate `settings.json` and `problems.json` in the `data` folder:
`python3 app.py`

4. Modify `settings.json` and `problems.json` to change the port and add challenges.

5. Set up the server for production.

## MIT License
Copyright 2020 Strellic (Bryce Casaje)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
