# SepticApi

A simple web server hosting an endpoint which responds whether a property at a 
given location possesses a septic system to treat sewage. Developed as part of a design exercise issued by https://www.hometap.com/

# How to run

## Requirements

1. Download and install Python 3.7.0* or later
    - You can find and download the latest version from [the official Python website](https://www.python.org/downloads/)
2. Install the Django web framework
    - You can download Django using the following terminal command after you install Python:

    > pip install django

## Starting the server

Start the server using the manage script

    > python manage.py runserver

**Optional:** Test the 3rd party API Postman mock server by visiting https://62292a2f-c5e4-4efc-a0ba-f9c563c7890b.mock.pstmn.io/

## Usage

Open a web browser and begin using the API by making calls to the http://localhost:8000/home/septic endpoint

The endpoint accepts two required query parameters

    1. address - the street address of the property
    2. zipcode - the zipcode of the property

The returned response indicates whether the property located at the given address and zipcode has a septic system

**Example:**
Request: http://localhost:8000/home/septic?address=122+Main+St&zipcode=94132

Response: 

```json
{ "septic": true }
```

**Note:** 122 Main St at zipcode 94132 is currently the only property known to the API that has a septic system

*The implementation makes use of Ordered Dictionaries which were added in Python 3.6 and officially declared a feature in Python 3.7