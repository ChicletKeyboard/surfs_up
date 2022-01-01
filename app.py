# import dependencies
from flask import Flask

# Create new flask instance caled app
app = Flask(__name__)

# Create root of routes
@app.route('/')
# add function hello_world
def hello_world():
    return 'Hello World'

# Run on windows --> navigate to console of where file is --> use 'set FLASK_APP = app.py'
## then do 'python -m flask run'
