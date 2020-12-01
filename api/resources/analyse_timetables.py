## Imports
from flask import request
from flask_restful import Resource, abort
from flask_jsonpify import jsonify
from webargs import fields
from webargs.flaskparser import use_args
from shared import db, asgard_services
import requests

class AnalyseTimetables(Resource):
    def get(self):
        ## Calculate the maximum number of sessions per week that are bookable
        maxSessionsPerHour = 2
        bookableSessionsPerWeek = ((5 * (9 * maxSessionsPerHour)) * 13) ## 5 working days, 9 hours per day, 13 weeks a semester

        ## Make a request to Mimir
        mimirResponse = requests.get(asgard_services['mimir'] + "/timetables")
        if mimirResponse.status_code != 200:
            abort(503, message="Mimir API is currently unavailable")
        timetables = mimirResponse.json()['data']['timetables']

        ## Iterate through each timetable and its bookings, calculating the statistics we are recording and add them to our stats array
        analysisResults = []
        for timetable in timetables:
            ## Calculate the sum of the booked durations. Mimir gives duration in hours, so adjust for how many sessions per hour we sets
            totalDurationBooked = 0
            for booking in timetable['bookings']:
                totalDurationBooked += (booking['duration'] * maxSessionsPerHour)
            ## Record the stats to a dict, this maps directly as a JSON object
            timetableStats = {
                "timetable": timetable['timetable'],
                "duration_booked": totalDurationBooked,
                "duration_bookable": bookableSessionsPerWeek,
                "booked_percent": float("{0:.2f}".format((totalDurationBooked / bookableSessionsPerWeek) * 100))
            }
            ## Push the statistics dict to the array
            analysisResults.append(timetableStats)

        ## Create our response structure ready for jsonify
        response = {
            "meta": {},
            "links": {
                "self": request.url
            },
            "data": {
                "timetables": analysisResults
            }
        }

        ## Convert the response into an actual JSON schema
        return jsonify(response)
