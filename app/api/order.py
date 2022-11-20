from app import app, db
from app.api.auth import auth, g
from flask import jsonify
from app.models import Order
from app.api.errors import bad_request
from datetime import date, timedelta, datetime
number_of_tables = 10


@app.route('/api/order')
@auth.login_required
def get_resource():
    return jsonify({'data': 'Hello, %s. Welcome to our restaurant!' % g.user.username})


@app.route('/api/order/preorder/<int:table_id>/<date_order>')
@auth.login_required
def pre_order(table_id, date_order):
    # Convert string date_order to date type:
    date_value = datetime.strptime(date_order, "%d-%m-%Y").date()
    if table_id > number_of_tables:
        return bad_request('This id is out of our restaurant range. We have only %d tables' %number_of_tables)
    if date_value < date.today():
        return bad_request('This day has passed, please enter a valid date!')
    if date_value > date.today() + timedelta(days=5):
        return bad_request('The order is valid within the next 5 days')

    # Convert date type to string to store in DB
    date_check = date_value.strftime("%d-%m-%Y")

    order = Order.query.filter_by(table_id=table_id, date_order=date_check).first()
    if order is None:
        new_order = Order(table_id=table_id, username=g.user.username, status='booked', date_order=date_check)
        g.user.bonus += 1
        db.session.add(new_order)
        db.session.commit()
        return jsonify({'data': '%s has successfully ordered table %d' % (g.user.username, table_id)})
    else:
        return jsonify({'data': 'So sorry that table %d has been already ordered, please choose another one' % table_id})


@app.route('/api/order/check/<int:table_id>/<date_order>')
@auth.login_required
def check_table(table_id, date_order):
    # Convert string date_order to date type:
    date_value = datetime.strptime(date_order, "%d-%m-%Y").date()
    if table_id > number_of_tables:
        return bad_request('This id is out of our restaurant range. We have only %d tables' % number_of_tables)
    if date_value < date.today():
        return bad_request('This day has passed, please enter a valid date!')
    if date_value > date.today() + timedelta(days=5):
        return bad_request('The order is valid within the next 5 days')

    # Convert date type to string to store in DB
    date_check = date_value.strftime("%d-%m-%Y")

    order = Order.query.filter_by(table_id=table_id, date_order=date_check).first()
    if order is None:
        return jsonify({'data': 'Table %d is free. You can pick it up!' % table_id})
    else:
        return jsonify({'data': 'So sorry that table %d has been already ordered, please choose another one' % table_id})
