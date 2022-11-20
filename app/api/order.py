from app import app, db
from app.api.auth import auth, g
from flask import jsonify
from app.models import Order

number_of_tables = 5


@app.route('/api/order')
@auth.login_required
def get_resource():
    return jsonify({'data': 'Hello, %s. Welcome to our restaurant!' % g.user.username})


@app.route('/api/order/preorder/<int:id>')
@auth.login_required
def pre_order(id):
    if id > number_of_tables:
        return jsonify({'data': 'Our restaurant has only %d tables. Sorry for this inconvenience!' % number_of_tables})
    order = Order.query.get(id)
    if not order:
        new_order = Order(id=id, username=g.user.username, status=True)
        g.user.bonus += 1
        db.session.add(new_order)
        db.session.commit()
        return jsonify({'data': '%s has successfully ordered table %d' % (g.user.username, id)})
    else:
        return jsonify({'data': 'So sorry that table %d has been already ordered, please choose another one' % id})


@app.route('/api/order/check/<int:id>')
@auth.login_required
def check_table(id):
    if id > number_of_tables:
        return jsonify({'data': 'Our restaurant has only %d tables. Sorry for this inconvenience!' % number_of_tables})
    order = Order.query.get(id)
    if not order:
        return jsonify({'data': 'Table %d is free. You can pick it up!' % id})
    else:
        return jsonify({'data': 'So sorry that table %d has been already ordered, please choose another one' % id})
