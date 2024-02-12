# Backend Senior Project
Built with [FastAPI](https://fastapi.tiangolo.com/)

### Basic setup
This documentation uses Pipenv as package manager
Use `pipenv shell` to create new python virtual environment

- Installing package
```bash
# using pipenv
pipenv install
# or pip
pip install requirements.txt
```
- Changing executable permission
```bash
chmod +x run_debug.sh
```
- Run the server
```bash
# using bash
./run_debug.sh
# or
uvicorn main:app --host 0.0.0.0 --port 3002 --reload
```

### Usage
By default the server is running on http://localhost:3002. Swagger API Documentation can be accessed in http://localhost:3002/docs
