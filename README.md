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
* python -m unittest discover -s integration_tests/ -p '*_test.py' -t ./

## To run all tests
* start the tequila_server
* python -m unittest discover -v -p '*_test.py'

## Coverage.
For now generates coverage for everything, need to change it to skip lib.

* sudo pip install coverage
* coverage run run_unit_tests.py
* coverage html -d coverage_html --omit=lib



