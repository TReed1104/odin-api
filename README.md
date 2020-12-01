# Odin, Utilisation and Usage Analyser
## What is Odin?
Odin is a service developed for analysing the utilisation of the facilities and functionality of the service in the Asgard System Stack.

<br>

---

## Repository Structure
UNDER CONSTRUCTION

<br>

---

## Dependencies
Odin uses the pip3 package manager and is written using Python3.

The following packages are used in the project:

### Flask - 1.0.3
Flask is the web microframework the application was developed to use as its core. It supplies all the main functionality and networking.

### Flask-RESTful - 0.3.7
Flask-RESTful is an extension to the Flask framework allowing for the easy configuration of REST architecture APIs. This handles our endpoint definition and opening the application up to the different query verb types.

### mysqlclient - 1.4.2.post1
MySQL client is required for SQLAlchemy to interact with MySQL databases.

### Flask-SQLAlchemy - 2.4.0
Flask-SQLAlchemy is a Flask wrapper for the Object-Relational Mapper, SQLAlchemy. SQLAlchemy provides the toolset we use to interact with the MySQL database at the back-end of Odin and provide a layer of security between the API and the raw data itself.

### Flask-Jsonpify - 1.5.0
Jsonify is our json parser, this package is what converts our result data from the database into the JSON responses we reply to our connected clients.

### Flask-Cors - 3.0.8
Flask-Cors is an extension package for routing and managing Cross-Origin Resource Sharing (CORS) across the application, and is mainly used to allow our web client to interact with the API itself.

### Webargs - 5.3.2
Webargs handles the parameter parsing from the endpoint URLs to usable data within our Flask resource objects, this library replaces the now depreciated "reqparse" from Flask-RESTful.

### Marshmellow - 3.0.1
Marshmellow is a dependency of Webargs, we had to freeze this at this version due to something on their end stopping working correctly.

<br>

---

## Commands
### Pip3
Batch Install the Pip3 modules at their frozen version by the following commands whilst in the projects root directory.
```pip3
pip3 install -r api/requirements.txt
```
