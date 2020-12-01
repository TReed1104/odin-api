## Imports
from flask import request
from flask_restful import Resource, abort
from flask_jsonpify import jsonify
from webargs import fields
from webargs.flaskparser import use_args
from shared import db, asgard_services
import requests

class AnalyseCarousels(Resource):
    def get(self):
        ## Make a request to Yggdrasil
        yggdrasilResponse = requests.get(asgard_services['yggdrasil'] + "/carousels")
        if yggdrasilResponse.status_code != 200:
            abort(503, message="Yggdrasil API is currently unavailable")
        carousels = yggdrasilResponse.json()['data']['carousels']

        ## Totals for all carousels
        totalContentDuration = 0
        totalNumberOfSlides = 0

        ## Analyse each carousel
        statisticsArray = []
        for carousel in carousels:
            ## Record the statistics for the current carousel
            carouselStats = {
                "id": carousel['id'],
                "name": carousel['name'],
                "carousel_duration": carousel['total_duration'],
                "number_of_content": len(carousel['content'])
            }
            statisticsArray.append(carouselStats)

            ## Total up carousel data
            totalContentDuration += carousel['total_duration']
            totalNumberOfSlides += len(carousel['content'])

        ## Create our response
        response = {
            "meta": {},
            "links": {
                "self": request.url
            },
            "data": {
                "totals": {
                    "number_of_carousels": len(carousels),
                    "total_content_duration": totalContentDuration,
                    "total_number_of_slides": totalNumberOfSlides
                },
                "carousels": statisticsArray
            }
        }

        ## Convert the response to an actual JSON format
        return jsonify(response)
