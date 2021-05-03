
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

data = {'name': 'Name1888',
        'street': 'Street_232334333',
        'rooms': 33,
        'price': '122345',
        'status': 'true',
        }

headers = {'Content-type': 'application/json'}
url = "https://admin-advertisement.herokuapp.com/api/advertisements"

# [{"_id":"E11yIyWbBB9PgTGi"},{"_id":"YWjtDiIIgxg3LROp"},{"_id":"dHtc6SZ7xVrxNZhp"},{"_id":"wA5igkWSSIB4quBJ"}]

r = requests.post(url=url,
                 json=data)
print(r.status_code)
print(r.text)
#r1 = requests.get(url=url, params={'id': 'wA5igkWSSIB4quBJ'})
#print(r1.headers)
#print(f'--> {r1.json()[0]}')