# Odin API
## What is Odin?
Odin is a service developed for analysing the utilisation of the facilities and functionality of the service in the Asgard System Stack.

<br>

---

## Repository Structure
UNDER CONSTRUCTION

<br>

---

## Dependencies
The template uses the pip3 package manager and is written using Python3.

The following packages are used in the project:

### API - Flask - 1.0.3
Flask is the web microframework the application was developed to use as its core. It supplies all the main functionality and networking.

### API - Flask-RESTful - 0.3.7
Flask-RESTful is an extension to the Flask framework allowing for the easy configuration of REST architecture APIs. This handles our endpoint definition and opening the application up to the different query verb types.

### API - mysqlclient - 1.4.6
MySQL client is required for SQLAlchemy to interact with MySQL databases.

### API - Flask-SQLAlchemy - 2.4.0
Flask-SQLAlchemy is a Flask wrapper for the Object-Relational Mapper, SQLAlchemy. SQLAlchemy provides the toolset we use to interact with the MySQL database used by the API and provide a layer of security between the API and the raw data itself.

### API - Flask-Jsonpify - 1.5.0
Jsonify is our json parser, this package is what converts our result data from the database into the JSON responses we reply to our connected clients.

### API - Flask-Cors - 3.0.8
Flask-Cors is an extension package for routing and managing Cross-Origin Resource Sharing (CORS) across the application, and is mainly used to allow our web client to interact with the API itself.

### API - Webargs - 5.3.2
Webargs handles the parameter parsing from the endpoint URLs to usable data within our Flask resource objects, this library replaces the now depreciated "reqparse" from Flask-RESTful.

### API - Marshmellow - 3.0.1
Marshmellow is a dependency of Webargs, we had to freeze this at this version due to something on their end stopping working correctly.

### API - Nose2 - 0.9.1
Nose2 is an extension of the Python Unit-test module, we use this as part of our unit, feature and integration testing. The project is set to export the results of these tests as JUnit XML files.

### API - Requests - 2.22.0
Requests is a library used for easily implementing HTTP GET/PUSH/POST/DELETE requests in python. Its through this package that the API requests data from the other APIs in the stack.

<br>

---

## Commands
### Pip3
Batch Install the Pip3 modules at their frozen version by the following commands whilst in the projects root directory.
```pip3
pip3 install -r api/requirements.txt
```

<br>

---

## Testing
Under Construction

<br>

---

## Installation
Under Construction

<br>

---

## Usage Guide - API Interactions and Endpoints

### Exposed Endpoints
Valid Endpoints
```
<server_address>/odin-api/analyse_timetables
<server_address>/odin-api/analyse_rooms
<server_address>/odin-api/analyse_carousels
<server_address>/odin-api/computers
```

Example Endpoints
```
10.5.11.173/odin-api/analyse_timetables
10.5.11.173/odin-api/analyse_rooms
10.5.11.173/odin-api/analyse_carousels
10.5.11.173/odin-api/computers
```

### Endpoint - Timetable Analysis
Usage:
```
<server_address>/odin-api/analyse_timetables

Supported HTTP Methods
* GET
```

params:
```
N/A
```

#### GET method
The GET method for the Timetable analysis endpoint returns a JSON array listing the statistics for each timetable.

Usage:
```
GET -> <server_address>/odin-api/analyse_timetables
```

Example Response:
```JSON
{
    "meta":{},
    "links":{
        "self": "http://odin-api:5000/analyse_timetables"
    },
    "data": {
        "timetables":[
            {
                "booked_percent": 223.5,
                "duration_bookable": 1170,
                "duration_booked": 2615.0,
                "timetable": "Timetable A"
            }
        ]
    }
}
```

### Endpoint - Room Analysis
Usage:
```
<server_address>/odin-api/analyse_rooms

Supported HTTP Methods
* GET
```

params:
```
N/A
```

#### GET method
The GET method for the Room analysis endpoint returns a JSON array listing the statistics for each room.

Usage:
```
GET -> <server_address>/odin-api/analyse_rooms
```

Example Response:
```JSON
{
    "meta":{},
    "links":{
        "self": "http://odin-api:5000/analyse_rooms"
    },
    "data": {
        "rooms":[
            {
                "id": 1,
                "name": "Room A",
                "percentiles":{
                    "percent_desks_used_in_teaching": 100,
                    "percent_desks_with_computers": 100,
                    "percent_teaching_desks_with_computers": 100
                },
                "totals":{
                    "number_of_capacity": 2,
                    "number_of_computers": 2,
                    "number_of_desks": 2
                }
            },
        ],
        "percentiles":{
            "percent_desks_used_in_teaching": 100,
            "percent_desks_with_computers": 100,
            "percent_teaching_desks_with_computers": 100
        },
        "totals":{
            "number_of_computers": 2,
            "number_of_desks": 2,
            "number_of_rooms": 1,
            "teaching_capacity": 2
        }
    }
}
```

### Endpoint - Carousel Analysis
Usage:
```
<server_address>/odin-api/analyse_carousels

Supported HTTP Methods
* GET
```

params:
```
N/A
```

#### GET method
The GET method for the carousel analysis endpoint returns a JSON array listing the statistics for each carousel.

Usage:
```
GET -> <server_address>/odin-api/analyse_carousels
```

Example Response:
```JSON
{
    "meta":{},
    "links":{
        "self": "http://odin-api:5000/analyse_carousels"
    },
    "data": {
        "carousels":[
            {
                "carousel_duration": 30000,
                "id": 1,
                "name": "Carousel A",
                "number_of_content": 2
            },
            {
                "carousel_duration": 15000,
                "id": 2,
                "name": "Carousel B",
                "number_of_content": 1
            },
        ],
        "totals":{
            "number_of_carousels": 2,
            "total_content_duration": 45000,
            "total_number_of_slides": 3
        }
    }
}
```

