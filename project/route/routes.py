from flask import Blueprint, render_template, redirect, request, url_for
from .way import Way
from markupsafe import escape

# Defining a blueprint
way_bp = Blueprint(
    'way_bp', __name__,
    template_folder='templates'
)

@way_bp.route('/insert', methods=['POST'])
def insert():
    try:
        route = Way.get_route_nationale(request.form['route'])
        route.set_point_kilometrique(request.form['depart'], request.form['arrive'])
        route.set_niveau(request.form['niveau'])
        route.insert()
        return render_template('formulaire.html', page="insert", route=None)
    except Exception as e:
        return render_template('formulaire.html', error=e, page="insert", route=None)


@way_bp.route('/liste', methods=['POST'])
def show():
    route = Way.get_route_nationale(request.form['route'])
    try:
        route.set_point_kilometrique(request.form['depart'], request.form['arrive'])
        return render_template('formulaire.html', route=route, page="show")
    except Exception as e:
        return render_template('formulaire.html', route=None, error=e, page="show")


@way_bp.route('/formulaire')
def formulaire():
    return render_template('formulaire.html', page=request.args.get('page'), route=None)