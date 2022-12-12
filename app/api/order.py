from app import app, db
from app.api.auth import auth, g
from flask import jsonify, request
from app.models import Order
from app.api.errors import bad_request
from datetime import date, timedelta, datetime

# Number of tables in our restaurant
number_of_tables = 10


# Home page
@app.route('/order', methods=['GET'])
@auth.login_required
def get_resource():
    date_check = date.today().strftime("%d-%m-%Y")
    count_ordered_table = Order.query.filter_by(date_order=date_check).count()
    number_of_tables_left = number_of_tables - count_ordered_table
    return jsonify({'data': 'Hello, %s. Welcome to our restaurant! There are %d tables left today. Order them now' % (
        g.user.username, number_of_tables_left)})


# Preorder a table by table id and the date
@app.route('/order/preorder/<int:table_id>/<date_order>', methods=['GET'])
@auth.login_required
def pre_order(table_id, date_order):
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
        new_order = Order(table_id=table_id, username=g.user.username, status='booked', date_order=date_check)
        g.user.bonus += 1
        db.session.add(new_order)
        db.session.commit()
        return jsonify({'data': '%s has successfully ordered table %d' % (g.user.username, table_id)})
    else:
        return jsonify(
            {'data': 'So sorry that table %d has been already ordered, please choose another one' % table_id})


# Check the status of the table by table id and the date
@app.route('/order/check/<int:table_id>/<date_order>', methods=['GET'])
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
        return jsonify(
            {'data': 'So sorry that table %d has been already ordered, please choose another one' % table_id})


# Get the status of your orders
@app.route('/order/status', methods=['GET'])
@auth.login_required
def check_status():
    data = Order.query.filter_by(username=g.user.username).all()
    if data is None:
        return jsonify({'data': 'You have not ordered any tables'})
    else:
        return jsonify(status=[i.serialize for i in data])


# Give your note to our restaurant to get a better service
@app.route('/order/status', methods=['PUT'])
@auth.login_required()
def put_note():
    data = request.get_json()
    if 'table_id' not in data or 'date_order' not in data or 'added_note' not in data:
        return bad_request(
            'Please enter valid information, including the table id, the date of order and the note of your'
            ' order to our restaurant')

    order = Order.query.filter_by(username=g.user.username, table_id=data['table_id'],
                                  date_order=data['date_order']).first()
    if order is None:
        return bad_request('Incorrect information')

    order.added_note = data['added_note']
    db.session.commit()
    return jsonify(adding_note=order.serialize)


# Cancel your order
@app.route('/order/status', methods=['DELETE'])
@auth.login_required()
def cancel_order():
    data = request.get_json()
    if 'table_id' not in data or 'date_order' not in data:
        return bad_request(
            'Please enter valid information, including the table id and the date of order')

    order = Order.query.filter_by(username=g.user.username, table_id=data['table_id'],
                                  date_order=data['date_order']).first()
    if order is None:
        return bad_request("Incorrect information")
    db.session.delete(order)
    db.session.commit()
    return jsonify({'data': 'You have already canceled this order'})

