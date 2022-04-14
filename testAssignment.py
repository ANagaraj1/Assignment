import requests
import json
import re

# https://gorest.co.in/public/v1/users?access-token=xxx
from requests.exceptions import InvalidJSONError


class GETRequest:
    def __init__(self, baseurl, endpoint, parameter):
        self.baseUrl = baseurl
        self.endpoint = endpoint
        self.parameter = parameter

    def invoke_get_method(self):
        #Invokes the URL and checks for valid JSON
        res = requests.get("https://" + self.baseUrl + self.endpoint + self.parameter)       #Invokes the GET API
        print("Response status code is "+str(res.status_code))
        try:
            return res.json()                           #validates the JSON response
        except:
            print("Invalid JSON")

    def verify_HTTP_response_code(self):
        try:
            res = requests.get("https://" + self.baseUrl + self.endpoint + self.parameter)  # Invokes the GET API
            if res.status_code == 200:                              #Checks for the desired status code
                print("\nReceived API response successfully")
            elif res.status_code == 401:                            #verifies if authentication is absent
                print("\nAuthentication required")
            elif res.status_code == 403:                            #verifies if request is unauthorized
                print("\nUnauthorized request")
            elif res.status_code == 500 :                           #verifies internal server error
                print("\nInternal Server Error")
            else:
                print("\nSome error occured")
        except:
            print("\nCould not get the API response")



    def check_pagination(self, api_response):
        # Verifies pagination field present in the GET response
        try:
            print("\nPagination value is "+str(api_response['meta']['pagination']))     #Tries to receive pagination value
        except KeyError as err:
            print("\npagination not present")

    def validate_email(self, api_response):
        # Validates the presence of email field in the response
        try :
            for i in api_response['data']:               #Checks for email by iterating through the data of each user
                pattern = r'\^[A-Za-z0-9._%+-^{|}]+@[A-Za-z0-9.-]+\.[A-Za-z0-9-]\b'
                match = re.match(pattern, i['email'])
                print("\nvalidated the email of user having email ID "+i['email'])
        except :
            print("\nEmail ID is not present")

    def validate_attributes(self, api_response):
        # Verifies if all entries on list data have similar attributes
        expected_keys = ['id', 'name', 'email', 'gender', 'status']
        try :
            for i in api_response['data']:               #Gets the data of each user
                actual_keys = []
                for key, value in i.items():
                    actual_keys.append(key)              #Gets all the attributes present for the user
                if actual_keys == expected_keys:
                    print("\nvalidated all the attributes of "+ i['name'])   #Checks if attributes are as same and as expected
                else:
                    print("\nActual and expected attributes are different for "+ i['name'])
        except Exception as e:
            print("\n Error occured", e)

    def api_without_authentication(self):
        res = requests.get("https://" + self.baseUrl + self.endpoint)
        status_code = res.status_code
        try:
            if status_code != 200:                         #Checks if incorrect status code is obtained when no authentication is provided
                print("\nObtained correct status code without giving access token")
            else:
                print("\nReceived incorrect status code as authentication was not provided")
        except:
            print("\n Error occured in GET API when executed without authentication")

    def verify_non_SSL(self):
        res = requests.get("http://" + self.baseUrl + self.endpoint + self.parameter)
        status_code = res.status_code
        try:
            if status_code != 200:                         #Checks if incorrect status code is obtained when wrong protocol is provided
                print("\nObtained correct status code while providing incorrect protocol")
            else:
                print("\nReceived incorrect status code on providing incorrect protocol")
        except:
            print("\n Error occured in GET API when executed with wrong protocol")





g1 = GETRequest("gorest.co.in/", "public/v1/users?", "access-token=")

api_response = g1.invoke_get_method()

g1. verify_HTTP_response_code()

g1.check_pagination(api_response)

g1.validate_email(api_response)

g1.validate_attributes(api_response)

g1.api_without_authentication()

g1.verify_non_SSL()


