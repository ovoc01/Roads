from flask import Blueprint, render_template, redirect, request, url_for
from .way import Way
from markupsafe import escape

# Defining a blueprint
way_bp = Blueprint(
    'way_bp', __name__,
    template_folder='templates'
)

@way_bp.route('/')
def index():
    return render_template('insert_route.html')


@way_bp.route('/insert', methods=['POST'])
def insert():
    try:
        route = Way.get_route_nationale(request.form['route'])
        route.set_point_kilometrique(request.form['depart'], request.form['arrive'])
        route.set_niveau(request.form['niveau'])
        route.insert()
        return redirect(url_for('way_bp.index'))
    except Exception as e:
        return render_template('formulaire.html', error=e)


@way_bp.route('/liste', methods=['GET'])
def show():
    ways = Way.get_liste_route_nationale()
    page = request.args.get('page')
    return render_template('liste_route.html', ways=ways, page=page)


@way_bp.route('/formulaire')
def formulaire():
    return render_template('formulaire.html', page=request.args.get('page'), route=request.args.get('route'))


@way_bp.route('/afficher', methods=['POST'])
def afficher():
    route = Way.get_route_nationale(request.form['route'])
    try:
        route.set_point_kilometrique(request.form['depart'], request.form['arrive'])
        return render_template('afficher_prix.html', route=route)
    except Exception as e:
        return render_template('afficher_prix.html', route=route, error=e)