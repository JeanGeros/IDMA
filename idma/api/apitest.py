import requests
import pprint
import socket
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


print(socket.gethostbyname(socket.gethostname()))
# token = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJjbGFzc29ubGl2ZSIsImRhdGEiOiJ7XCJlbWFpbFwiOlwiaWRtYS5jbGFzc29ubGl2ZUBpZG1hLmNsXCIsXCJpcFwiOlwiMTkyLjE2OC44LjI0OVwifSJ9.B2JvddO1RyMKBLCH7aVctr-CXqGSQS57bCzOifgv4tY"
# url = f'https://www.apiclassonlive.com/api/v1/${token}/content'
# data = requests.get(url)
# print(data.status_code)
# pprint.pprint(data.json())


# import http.client

# conn = http.client.HTTPSConnection("www.apiclassonlive.com")
# conn.request("GET", f"/api/v1/{token}/content")
# res = conn.getresponse()
# data = res.read()
# print(data.decode("utf-8"))

# email = "paolamonsalvr@gmail.com"
# conn = http.client.HTTPSConnection("www.apiclassonlive.com")
# conn.request("GET", f"/api/v1/{token}/username/{email}")
# res = conn.getresponse()
# data = res.read()
# print(data.decode("utf-8"))

# # 192.168.8.249
@csrf_exempt
def webhook(request):
    sessions= ['TICS','MATEMATICAS','EX.ORAL  Y ESCRITA','BIOLOGIA','QUIMICA','FISICA']
    token = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJjbGFzc29ubGl2ZSIsImRhdGEiOiJ7XCJlbWFpbFwiOlwiaWRtYS5jbGFzc29ubGl2ZUBpZG1hLmNsXCIsXCJpcFwiOlwiMTkyLjE2OC44LjI0OVwifSJ9.B2JvddO1RyMKBLCH7aVctr-CXqGSQS57bCzOifgv4tY'
    if request.method == 'POST':
        data = request.body
        pprint.pprint(data.decode("utf-8"))

        response = requests.put(f"https://www.apiclassonlive.com/api/v1/{token}/particular/{sessionid}/addstudent", params=data)
        pprint.pprint(response.json())

        return HttpResponse("Webhook recibido!")