import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores, items

blp = Blueprint("stores", __name__, description='actions on store db')

@blp.route("/store/<string:store_id>")
class Store(MethodView):
    def get(self, store_id):
        try:
            return stores[store_id]
        except:
            abort(404, 'Store not found')

    def delete(self, store_id):
        try:
            stores.pop(store_id)
            return {'msg': 'deleted successfully'}, 204
        except:
            abort(404, 'Item not found')

@blp.route("/store/<string:store_id>/items")
class Store(MethodView):
    def get(self, store_id):
        if store_id not in stores:
            abort(404, 'Store not found')
        return [item for item in list(items.values()) if item["store_id"]==store_id]

@blp.route("/store")
class StoreList(MethodView):
    def get(self):
        return {"stores": list(stores.values())}
    
    def post(self):
        request_data = request.get_json()
        store_id = uuid.uuid4().hex
        stores[store_id] = {**request_data, 'id': store_id}
        return stores[store_id], 201