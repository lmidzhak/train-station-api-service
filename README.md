# **Train Station API Service**

## Project Overview

The system provides functionalities for creating and managing train station tickets, orders, journeys, routes, etc.

## **Features**

* Creating train types, trains with crew, train stations, routes and journeys
* Managing orders and tickets
* Filtering journeys by arrival/departure date, by source/destination stations
* JWT Authenticated
* Admin panel /admin/
* Documentation is located at api/doc/swagger/

## Installation & Run

### Prerequisites:

* Python 3.8+ 
* Docker Desktop

Set environment variable:

* Copy and rename the .env.sample file to .env
* Open the .env file and edit the environment variables
* Save the .env file securely
* Make sure the .env file is in .gitignore

### On Windows:

* python -m venv venv
* venv\Scripts\activate

### On UNIX or macOS:

* python3 -m venv venv 
* source venv/bin/activate

### Install requirements

* docker-compose up --build
* (Optional) Create a superuser

* If you want to perform all available features, create a superuser account in a new terminal:
* docker-compose exec -it airport /bin/sh
* python manage.py createsuperuser
* Go to site http://127.0.0.1:8002/
