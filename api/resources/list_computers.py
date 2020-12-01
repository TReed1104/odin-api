## Imports
from flask import request
from flask_restful import Resource, abort
from flask_jsonpify import jsonify
from webargs import fields
from webargs.flaskparser import use_args
from shared import db, asgard_services
from models.computer_utilisation import ComputerUtilisation

class ListComputers(Resource):
    def get(self):
        ## Get all the computers in the Computer Utilisation table
        computers = ComputerUtilisation.query.all()
        computersArray = []
        ## Check we found any results
        if computers is not None:
            computersArray = [computer.serialize for computer in computers]
        ## Formulate the response
        response = {
            "meta": {},
            "links": {
                "self": request.url
            },
            "data": {
                "computers": computersArray
            }
        }
        ## Convert the list of computers into a json response
        return jsonify(response)
