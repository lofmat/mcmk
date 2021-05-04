
"""
This follows the REST pattern.

We have two flows:

1. Create new advertisement
2. Edit any existing advertisement
What you need to do API + E2E testing:
1. Create test cases for flow above
2. Implement scenarios for created cases

please upload your solution to github.com and share the link with us.

● Feel free to use any programming language, framework, library and
package you prefer
● Use any structure or pattern you’re comfortable with
● Include a README file, in which you explain how to set up the project, how to
run tests etc.
"""

import requests

data = {'name': 'Name2',
        'street': 'Street_232334333',
        'rooms': 33,
        'price': '122345',
        'status': 'true',
        }

data1 = {'name': 'Name1',
        'street': 'Street_3223232334333',
        'rooms': 331,
        'price': '12322345',
        'status': 'true',
        }

headers = {'Content-type': 'application/json'}
url = "https://admin-advertisement.herokuapp.com/api/advertisements"

# [{"_id":"E11yIyWbBB9PgTGi"},{"_id":"YWjtDiIIgxg3LROp"},{"_id":"dHtc6SZ7xVrxNZhp"},{"_id":"wA5igkWSSIB4quBJ"}]

ox = requests.get(url)
print(ox.json)
for i in ox.json():
    print(i)
    requests.delete(url, params={'_id':i['_id']})
# requests.post(url, data)
# requests.post(url, data1)
# r = requests.get(url=url)
# print(r.status_code)
# print(r.text)
# for i in r:
#     print(i)
#     requests.delete(url)
#r1 = requests.get(url=url, params={'id': 'wA5igkWSSIB4quBJ'})
#print(r1.headers)
#print(f'--> {r1.json()[0]}')


# @pytest.mark.parametrize("data", [[('2020-10-17', 1, 2), ('2020-10-15', 0, 1), ('2020-10-14', 1, 1)]])
# @pytest.fixture(autouse=True)
# def run_around_tests(some_url):
#     # Code that will run before your test, for example:
#     try:
#         r = requests.get(some_url) # ... do something to check the existing files
#         if r.text:
#             return False
#         logging.info(f'{r.status_code} - OK')
#     except Exception as e:
#         logging.error(f'{e} - NOK')
#         return False
#     logging.info('End before test')
#     yield
#     for ad in requests.get(some_url):
#         requests.delete(url=some_url, )
