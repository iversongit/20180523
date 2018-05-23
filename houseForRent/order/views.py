from flask import Blueprint, request, jsonify, session, render_template
from user.models import Order, House, User
from utils import status_code
from datetime import datetime
order_blueprint = Blueprint("order",__name__)

@order_blueprint.route("/",methods=["POST"])
def orders():
    order_dict = request.form
    house_id = order_dict.get('house_id')
    start_time = order_dict.get('start_time')
    end_time = order_dict.get('end_time')
    start_time = datetime.strptime(start_time,"%Y-%m-%d") # str --> datetime
    end_time = datetime.strptime(end_time,"%Y-%m-%d")

    if not all([house_id,start_time,end_time]):
        return jsonify(status_code.PARAMS_ERROR)

    if start_time > end_time:
        return jsonify(status_code.ORDER_START_TIME_GT_END_TIME)

    house = House.query.get(house_id)

    order = Order()
    order.user_id = session['user_id']
    order.house_id = house_id
    order.begin_date = start_time
    order.end_date = end_time
    order.house_price = house.price
    order.days = (end_time - start_time).days + 1
    order.amount = order.days * order.house_price

    try:
        order.add_update()
        return jsonify(status_code.SUCCESS)
    except:
        return jsonify(status_code.DATABASE_ERROR)

@order_blueprint.route('/order/',methods=['GET'])
def order(): # 返回所有订单
    return render_template('orders.html')

@order_blueprint.route('/showorders/',methods=['GET'])
def showorders():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        orders = user.orders
        order_list = []
        for order in orders:
            order_list.append(order.to_dict())
        return jsonify(code=status_code.OK,orders=order_list)

@order_blueprint.route('/lorders/',methods=['GET'])
def lorders(): # 返回所有订单
    return render_template('lorders.html')

@order_blueprint.route('/customer_lorders/',methods=['GET'])
def customer_lorders():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        houses = user.houses
        order_list = []
        for house in houses:
            orders = house.orders
            for order in orders:
                order_list.append(order.to_dict())
        return jsonify(code=status_code.OK,orders=order_list)

@order_blueprint.route("/change_status/",methods=['PUT'])
def change_status():
    status_list = request.form
    status = status_list.get('status')
    order_id = status_list.get('order_id')
    order = Order.query.get(order_id)
    if status == '0':
        order.status = "WAIT_COMMENT"
    elif status == '1':
        order.status =  "REJECTED"
    try:
        order.add_update()
        return jsonify(code=status_code.OK,status=order.status)
    except Exception as e:
        return jsonify(status_code.DATABASE_ERROR)

