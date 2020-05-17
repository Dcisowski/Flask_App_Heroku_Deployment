# -*- coding: utf-8 -*-

from flask_restful import Resource
from flask_jwt import jwt_required
from models.store import StoreModel


class Store(Resource):
    @jwt_required()
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': 'Store not found'}, 404


    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}
        
        store = StoreModel(name)

        try:
            store.save_to_db()
        except:
            return {"message": "An error occurred creating the store."}

        return store

    
    @jwt_required()
    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
        
        return {'message': 'Store Deleted'}

class StoreList(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}
