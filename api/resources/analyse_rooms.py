## Imports
from flask import request
from flask_restful import Resource, abort
from flask_jsonpify import jsonify
from webargs import fields
from webargs.flaskparser import use_args
from shared import db, asgard_services
import requests

class AnalyseRooms(Resource):
    def get(self):
        ## Make a request to Heimdall
        heimdallResponse = requests.get(asgard_services['heimdall'] + "/rooms")
        if heimdallResponse.status_code != 200:
            abort(503, message="Heimdall API is currently unavailable")
        rooms = heimdallResponse.json()['data']['rooms']

        ## Calculate the stats about the rooms
        totalDesks = 0
        totalTeachingCapacity = 0
        totalComputers = 0
        roomByRoomStatistics = []

        ## Iterate through each room, calculating its stats
        for room in rooms:
            ## Stats for this room
            roomStatistics = {
                "id": room["id"],
                "name": room['name'],
                "totals": {
                    "number_of_desks": room['number_of_desks'],
                    "number_of_computers": room['number_of_computers'],
                    "number_of_capacity": room['capacity']
                },
                "percentiles": {
                    "percent_desks_used_in_teaching": float("{0:.2f}".format(((room['capacity'] if room['capacity'] > 0 else 1 ) / room['number_of_desks']) * 100)),
                    "percent_desks_with_computers": float("{0:.2f}".format((room['number_of_computers'] / room['number_of_desks']) * 100)),
                    "percent_teaching_desks_with_computers": float("{0:.2f}".format((room['number_of_computers'] / room['capacity']) * 100))
                }
            }
            ## Push the statistics object to the array
            roomByRoomStatistics.append(roomStatistics)

            ## Tally the total statistics for all the rooms registered with the system
            totalDesks += room['number_of_desks']
            totalTeachingCapacity += room['capacity']
            totalComputers += room['number_of_computers']

        ## Create our response
        response = {
            "meta": {},
            "links": {
                "self": request.url
            },
            "data": {
                "totals": {
                    "number_of_rooms": len(rooms),
                    "number_of_desks": totalDesks,
                    "number_of_computers": totalComputers,
                    "teaching_capacity": totalTeachingCapacity,
                },
                "percentiles": {
                    "percent_desks_used_in_teaching": float("{0:.2f}".format((totalTeachingCapacity / totalDesks) * 100)),
                    "percent_desks_with_computers": float("{0:.2f}".format((totalComputers / totalDesks) * 100)),
                    "percent_teaching_desks_with_computers": float("{0:.2f}".format((totalComputers / totalTeachingCapacity) * 100))
                },
                "rooms": roomByRoomStatistics
            }
        }

        ## Convert the response to an actual JSON format
        return jsonify(response)
