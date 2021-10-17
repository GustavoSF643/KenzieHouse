from app.models.fiscal_note_model import FiscalNote
from app.models.order_model import OrderModel
from app.exceptions.order_exc import OrderNotFound, UnauthorizedUserAcess
from app.exceptions.fiscal_note_exc import InvalidOrderStatusError
from flask_jwt_extended import jwt_required, get_current_user
from flask import jsonify
from http import HTTPStatus

@jwt_required()
def download_fiscal_note_by_order_id(order_id):
    user = get_current_user()

    try:
        order = OrderModel.order_verify(order_id)
        order.user_order_verify(user.user_id)

        if order.status != 'Pagamento Confirmado':
            raise InvalidOrderStatusError('Order has been canceled or invoice has not yet been paid!')

        shipping_company = order.shipping_company
        invoice = order.invoice
        buyer = order.user 

        data = {
            'shipping_company_name': shipping_company.name,
            'shipping_company_cnpj': shipping_company.cnpj,
            'shipping_value': invoice.shipping_value,
            'shipping_adress': order.adress,
            'products': order.orders_product,
            'total_value': invoice.value,
            'purcharse_date': order.created_at,
            'buyer_name': f'{buyer.name} {buyer.last_name}',
            'buyer_cpf': buyer.cpf,
            'buyer_email': buyer.email
        }

        fiscal_note = FiscalNote(**data)

        return jsonify(fiscal_note), HTTPStatus.OK

    except UnauthorizedUserAcess as e:
        return jsonify(error=str(e)), HTTPStatus.UNAUTHORIZED

    except OrderNotFound as e:
        return jsonify(error=str(e)), HTTPStatus.NOT_FOUND

    except InvalidOrderStatusError as e:
        return jsonify(error=str(e)), HTTPStatus.BAD_REQUEST
