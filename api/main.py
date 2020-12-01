## Imports
from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from models.computer_utilisation import ComputerUtilisation
from shared import db, asgard_services, task_interval, request_timeout
from resources import analyse_timetables, analyse_rooms, analyse_carousels, list_computers
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
import os
from datetime import datetime
import requests

## Create our Flask app and connect it to our database
app = Flask(__name__)
api = Api(app)
app.config.from_pyfile('configs/main.cfg')
CORS(app)
db.init_app(app)
with app.app_context():
    db.create_all()

## Register our endpoints for the API
api.add_resource(analyse_timetables.AnalyseTimetables, '/analyse_timetables')
api.add_resource(analyse_rooms.AnalyseRooms, '/analyse_rooms')
api.add_resource(analyse_carousels.AnalyseCarousels, '/analyse_carousels')
api.add_resource(list_computers.ListComputers, '/computers')

## Add each of the Asgard APIs we want to analyse to the global dictionary in the project
asgard_services['heimdall'] = app.config['HEIMDALL_API']
asgard_services['mimir'] = app.config['MIMIR_API']
asgard_services['yggdrasil'] = app.config['YGGDRASIL_API']
## Import the config settings to be shared across the app's resources
task_interval = app.config['TASK_INTERVAL']
request_timeout = app.config['REQUEST_TIMEOUT']

## Our Background task for analysing the Heimdall API
def AnalyseHeimdallComputers():
    print("Analysing the Computers registered with Heimdall, Call made at:", datetime.now())
    try:
        ## Form our GET request to the Heimdall API
        heimdallComputersUrl = asgard_services['heimdall'] + "/computers"
        response = requests.get(heimdallComputersUrl, timeout=request_timeout)
        ## Check the response status code is OK
        if response.status_code != 200:
            print("Response gave error code: ", response.status_code)
        ## Get the json data from the API response
        heimdallComputers = response.json()['data']['computers']
        ## Test print all the results in the response
        for computer in heimdallComputers:
            ## As we are outside of the Flask resource views, we have to manually use our SQLAclhemy context from the Flask App
            with app.app_context():
                ## Try and grab the corrseponding computer from Odin
                odinInstance = ComputerUtilisation.query.filter_by(mac_address=computer['mac_address'])
                ## If the Instance exists, update it, else create it
                if odinInstance.first() is None:
                    ## Map the Heimdall data to a new Odin instance
                    newComputerData = {}
                    ## The computer's mac address is the unique field, map it across to Odin
                    newComputerData['mac_address'] = computer['mac_address']
                    ## If the Computer is On, record it as being seen
                    if computer['status'] == "On":
                        newComputerData['last_seen'] = datetime.now()
                        newComputerData['seen_count_current'] = 1
                        newComputerData['seen_count_highest'] = 1
                        ## Depending on what OS the computer is, increment the right counter
                        if computer['os_name'] == "Windows":
                            newComputerData['os_count_windows'] = 1
                        elif computer['os_name'] == "Linux":
                            newComputerData['os_count_linux'] = 1
                        elif computer['os_name'] == "MacOS":
                            newComputerData['os_count_mac'] = 1
                        else:
                            newComputerData['os_count_unknown'] = 1
                    ## Create the instance using the dictionary of the Heimdall data
                    odinInstance = ComputerUtilisation(**newComputerData)
                    ## Push the data to the database
                    db.session.add(odinInstance)
                    db.session.commit()
                else:
                    ## Map the Heimdall data to the existing Odin instance
                    updatedComputerData = {}
                    updatedComputerData['mac_address'] = computer['mac_address']        ## The computer's mac address is the unique field, map it across to Odin
                    ## If the Computer is On, record it as being seen
                    if computer['status'] == "On":
                        ## Update the seen counters
                        updatedComputerData['last_seen'] = datetime.now()
                        updatedComputerData['seen_count_current'] = odinInstance.first().seen_count_current + 1
                        ## Check if the new seen counter is the new highest count
                        if updatedComputerData['seen_count_current'] > odinInstance.first().seen_count_highest:
                            updatedComputerData['seen_count_highest'] = updatedComputerData['seen_count_current']
                        ## Depending on what OS the computer is, increment the right counter
                        if computer['os_name'] == "Windows":
                            updatedComputerData['os_count_windows'] = odinInstance.first().os_count_windows + 1
                        elif computer['os_name'] == "Linux":
                            updatedComputerData['os_count_linux'] = odinInstance.first().os_count_linux + 1
                        elif computer['os_name'] == "MacOS":
                            updatedComputerData['os_count_mac'] = odinInstance.first().os_count_mac + 1
                        else:
                            updatedComputerData['os_count_unknown'] = odinInstance.first().os_count_unknown + 1
                    else:
                        ## If the computer is not currently on
                        updatedComputerData['seen_count_current'] = 0
                    ## Update the instance in the database using the new data in our mapped dictionary
                    odinInstance.update(updatedComputerData)
                    odinInstance.first().updated_at = datetime.now()
                    db.session.commit()

    except (requests.Timeout, requests.ConnectionError) as error:
        print("Request failed due to error:", error)

 ## Flask Dev mode technically spins up two instances of Flask, this check makes sure we don't start the scheduler twice
if not app.debug or os.environ.get("WERKZEUG_RUN_MAIN") == "true":
    scheduler = BackgroundScheduler()               ## Setup the background scheduled tasks
    scheduler.start()                               ## Stat the scheduler executing
    atexit.register(lambda: scheduler.shutdown())   ## Atexit handles the destruction of the scheduler tasks and closes the scheduler instance
    ## Register our background task
    print("Creating background task Heimdall_Analysis, triggering at an Interval of", task_interval, "seconds")
    scheduler.add_job(func=AnalyseHeimdallComputers, id='Heimdall_Analysis', trigger='interval', seconds=task_interval)

## Our Apps main entry point
if __name__ == '__main__':
    ## Initialise the application, 0.0.0.0 means to use our machine ip and enable debugging if needed
    app.run(host='0.0.0.0', port='5000')
