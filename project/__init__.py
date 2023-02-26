from flask import Flask, redirect, url_for
from route import routes

app = Flask(__name__)

app.register_blueprint(routes.way_bp, url_prefix='/route')

@app.route('/')
def index():
    return redirect(url_for('way_bp.formulaire') + '?page=show')

if __name__ == '__main__':
    app.run(debug=True, port=8000)