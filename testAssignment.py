import requests
import json

# https://gorest.co.in/public/v1/users?access-token=xxx
class GETRequest:
    def __init__(self, baseurl, endpoint, parameter):
        self.baseUrl = baseurl
        self.endpoint = endpoint
        self.parameter = parameter

    def invoke_get_method(self):
        res = requests.get("https://" + self.baseUrl + self.endpoint + self.parameter)
        print(res.status_code)
        assert res.status_code == 200, "Incorrect status code"
        return res.json()

    def check_pagination(self, api_response):
        try:
            print(api_response['meta']['pagination'])
        except KeyError as err:
            print("pagination not present")

    def validate_json(self, api_response):
        try:
            json_response1= json.dumps(api_response)
            json.loads(json_response1)
        except ValueError as err:
            return False
        return True

    def validate_email(self, api_response):
        for i in api_response['data']:
            assert i['email'] != None, "email not present"

    def validate_attributes(self, api_response):
        l1= ['id', 'name', 'email', 'gender', 'status']
        for i in api_response['data']:
            l2 = []
            for key, value in i.items():
                l2.append(key)
            assert l2 == l1, "the attributes are not the same"



g1 = GETRequest("gorest.co.in/", "public/v1/users?", "access-token=")
api_response = g1.invoke_get_method()
g1.check_pagination(api_response)
value = g1.validate_json(api_response)
print(value)
g1.validate_email(api_response)
g1.validate_attributes(api_response)


