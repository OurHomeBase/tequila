# tequila

# OAuth2

For now the only that is working is password grant. For now we don't need everything else.

To test it:
* install Rest Client
* start app
* POST http://localhost:8080/oauth/token
Authorization: Basic czZCaGRSa3F0MzpnWDFmQmF0M2JW
Content-Type: application/x-www-form-urlencoded
grant_type=password&username=sss&password=A3ddj3w&client_id=GbRmKgbSMmlE2NlugMeFfQIba8hoVyBFsWS8Igsq
* you will get access token
* make a request 
POST http://localhost:8080/api/me
Authorization: Bearer <YOUR ACCESS TOKEN>

If everything works properly you will get a user.

# Testing
## Unit Testing
* make sure app engine is installed in:
  /usr/local/google_appengine

* python run_unit_tests.py

## Integration Testing
* start the tequila_server
* python run_integration_tests.py

## To run all tests
* start the tequila_server
* python -m unittest discover -v -p '*_test.py'

## Coverage.
To install coverage tool on your machine:
sudo pip install coverage

To run coverage analysis and generate a report:
* coverage run run_unit_tests.py
* coverage html

Please note that the packages that are measured are listed in the file .coveragerc.
If you add a new package, please add it to the source parameter in .coveragerc file.
