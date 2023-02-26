from flask import Flask
from route import routes

app = Flask(__name__)

# Registering blueprints
app.register_blueprint(routes.way_bp, url_prefix='/route')

if __name__ == '__main__':
    app.run(debug=True, port=8000)
# from route.way import Way

# route = Way.get_route_nationale("RNP 7")
# route.set_arrive(7)
# route.set_depart(10)
# route.set_niveau(5)
# route.insert()