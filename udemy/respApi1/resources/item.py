import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import items, stores

blp = Blueprint("items", __name__, description='actions on item db')

@blp.route("/item/<string:item_id>")
class Store(MethodView):
    def get(self, item_id):
        try:
            return items[item_id]
        except:
            abort(404, 'item not found')

    def delete(self, item_id):
        try:
            items.pop(item_id)
            return {'msg': 'deleted successfully'}, 204
        except:
            abort(404, 'Item not found')

    def put(self, item_id):
        request_data = request.get_json()
        try:
            items[item_id]['name'] = request_data['name']
            items[item_id]['price'] = request_data['price']
            return items[item_id]
        except:
            abort(404, 'Item not found')

@blp.route("/item")
class StoreList(MethodView):
    def get(self):
        return {"stores": list(items.values())}
    
    def post(self):
        request_data = request.get_json()
        if request_data['store_id'] not in stores:
            abort(404, 'Store not found')
        item_id = uuid.uuid4().hex
        items[item_id] = {**request_data, 'item_id': item_id}
        return items[item_id], 201