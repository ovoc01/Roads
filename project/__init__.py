from flask import Flask
from route import routes

app = Flask(__name__)

app.register_blueprint(routes.way_bp, url_prefix='/route')

if __name__ == '__main__':
    app.run(debug=True, port=8000)