from flask import Flask
from src.models import Base, engine

app = Flask(__name__)
base.metadata.create_all(ingine)

if __name__ == '__main__':
    app.run(debug=True)