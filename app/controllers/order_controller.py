from flask import request, jsonify
from app.models.order_model import OrderModel
from app.models.adress_model import AdressModel
from flask_jwt_extended import (
    jwt_required,
    get_current_user
)
from http import HTTPStatus

@jwt_required()
def create_order():
    data_json = request.get_json()
    adress_id = data_json.pop('adress_id')
    adress = jsonify(AdressModel.query.get(adress_id))
    adress.pop('adress_id')

    # TODO -> Usar o dict adress para criar um novo endereço na tabela
    # order_adresses, depois de criada pegar seu id e adiconar ao data_json

    user = get_current_user()
    data_json['user_id'] = user.id

    order = OrderModel(**data_json)
    # user.orders.append(order)

    # order.save_self()
    
    return jsonify(order), HTTPStatus.CREATED


@jwt_required()
def read_order():
    user = get_current_user()

    return jsonify(user.orders), HTTPStatus.OK

@jwt_required()
def update_order(order_id):
    order = OrderModel.query.get(order_id)
    status = request.json.get('status')

    # TODO -> Verificar se somente o status esta sendo
    # atualizado

    # TODO -> Verificação se o user do token é o 
    # proprietario da order sendo atualizada

    order.status = status

    order.save_self()

    return jsonify(order), HTTPStatus.OK

@jwt_required()
def delete_order(order_id):
    # order = OrderModel.query.get(order_id)

    # TODO -> Deleção da order envolve varios cascade
    # deve-se montar eles no relationship primeiro

    # order.delete_self()

    return '', HTTPStatus.NO_CONTENT
