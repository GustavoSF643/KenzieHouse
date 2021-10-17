from flask import request, jsonify
from app.models.order_model import OrderModel
from app.models.adress_model import AdressModel
from app.models.order_adress_model import OrderAdressModel
from app.models.order_product_model import OrderProductModel
from app.models.product_model import ProductModel
from app.models.shipping_company_model import ShippingCompanyModel
from app.models.payment_method_model import PaymentMethodModel
from app.models.invoices_model import InvoiceModel
from flask_jwt_extended import jwt_required, get_current_user
from http import HTTPStatus
from dataclasses import asdict
from app.exceptions.order_exc import InvalidTypeError, UnauthorizedUserAcess, OrderNotFound
from app.exceptions.adress_exc import AdressNotFound
from app.exceptions.product_exc import ProductNotFound
from app.exceptions.shipping_company_exc import ShippingCompanyNotFound
from app.exceptions.payment_exc import PaymentMethodNotFound
from app.exceptions.invoice_exc import ExpiredInvoiceError

@jwt_required()
def create_order():
    data_json = request.json

    adress_id = data_json.pop('adress_id')

    try:
        shipping_company = ShippingCompanyModel.shipping_company_verify(data_json['shipping_company_id'])
        PaymentMethodModel.payment_method_verify(data_json['payment_method_id'])

        adress = asdict(AdressModel.adress_verify(adress_id))
        adress.pop('adress_id')

        order_adress = OrderAdressModel.order_adress_verify(adress)
        data_json['adress_id'] = order_adress.order_adress_id

        user = get_current_user()
        data_json['user_id'] = user.user_id

        cart_items = data_json.pop('products')

        for item in cart_items:
            ProductModel.product_verify(item['product_id'])

        order = OrderModel(**data_json)
        order.save_self()
        
        for item in cart_items:
            item['order_id'] = order.order_id
            order_product = OrderProductModel(**item)
            order_product.save_self()

        products_value = sum([item['total_value'] for item in cart_items])

        invoice = InvoiceModel(
            order_id=order.order_id, 
            shipping_value=shipping_company.minimum_shipping_price, 
            products_value=products_value,
            value=(products_value + shipping_company.minimum_shipping_price)
        )
        invoice.order = order
        invoice.save_self()

    except AdressNotFound as e:
        return jsonify(error=str(e)), HTTPStatus.NOT_FOUND
    
    except ProductNotFound as e:
        return jsonify(error=str(e)), HTTPStatus.NOT_FOUND
    
    except ShippingCompanyNotFound as e:
        return jsonify(error=str(e)), HTTPStatus.NOT_FOUND

    except PaymentMethodNotFound as e:
        return jsonify(error=str(e)), HTTPStatus.NOT_FOUND
    
    except InvalidTypeError as e:
        return jsonify(error=str(e)), HTTPStatus.BAD_REQUEST

    return jsonify(order), HTTPStatus.CREATED


@jwt_required()
def read_order():
    user = get_current_user()

    return jsonify(user.orders), HTTPStatus.OK

@jwt_required()
def get_invoice_by_order_id(order_id):
    user = get_current_user()
    
    try:
        order = OrderModel.order_verify(order_id)
        order.user_order_verify(user.user_id)

    except OrderNotFound as e:
        return jsonify(error=str(e)), HTTPStatus.NOT_FOUND

    except UnauthorizedUserAcess as e:
        return jsonify(error=str(e)), HTTPStatus.UNAUTHORIZED

    return order.invoice.format_self(), HTTPStatus.OK

@jwt_required()
def pay_invoice_by_order_id(order_id):
    user = get_current_user()
    
    try:
        order = OrderModel.order_verify(order_id)
        order.user_order_verify(user.user_id)
        order.invoice.verify_invoice_due_date()

    except OrderNotFound as e:
        return jsonify(error=str(e)), HTTPStatus.NOT_FOUND

    except UnauthorizedUserAcess as e:
        return jsonify(error=str(e)), HTTPStatus.UNAUTHORIZED

    except ExpiredInvoiceError as e:
        order.cancel_order()
        order.save_self()

        return jsonify(error=str(e), msg='Order was canceled due to non-payment'), HTTPStatus.BAD_REQUEST
    
    order.payment_confirm()
    order.save_self()

    return jsonify(order_status=order.status), HTTPStatus.OK