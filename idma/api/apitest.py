import requests
import pprint
import socket
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import http.client
import json
# url = "https://api.ipify.org"
# data = requests.get(url)
# ip = data._content
# print('My public IP address is: {}'.format(ip))


# token = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJjbGFzc29ubGl2ZSIsImRhdGEiOiJ7XCJlbWFpbFwiOlwiaWRtYS5jbGFzc29ubGl2ZUBpZG1hLmNsXCIsXCJpcFwiOlwiMTkwLjExNC4zNS4xNlwifSJ9.s55cKx9dGF4yI3P5Le0KevDLX5GEVVruyKbU5uGRH3M'


# email = "paolamonsalvr@gmail.com"
# conn = http.client.HTTPSConnection("www.apiclassonlive.com")
# conn.request("GET", f"/api/v1/{token}/username/{email}")
# res = conn.getresponse()
# data = res.read()
# print(data.decode("utf-8"))

# url = f'https://www.apiclassonlive.com/api/v1/{token}/content'
# data = requests.get(url)
# print(data.status_code)
# data = data.json()
# pprint.pprint(data)

# for d in data['contentList']:
    # if "Nivelación" in d['title']:
        # print(f"ID: {d['contentId']}")
        # print(f"Titulo: {d['title'].strip()}")
        # print(f"Tipo Contenido:  {d['contentType'].strip()}")
        # print(print(d))
        # print("------------------------------------")


# conn = http.client.HTTPSConnection("www.apiclassonlive.com")
# conn.request("GET", f"/api/v1/{token}/content")
# res = conn.getresponse()
# data = res.read()
# print(data.decode("utf-8"))


['MATEMATICAS', 'EXPRESION ORAL Y ESCRITA', 'QUIMICA', 'TICS', 'FISICA', 'BIOLOGIA']
# # 192.168.8.249

@csrf_exempt
def webhook(request):
    # Nombre de sesiones ['TICS','MATEMATICAS','EX.ORAL  Y ESCRITA','BIOLOGIA','QUIMICA','FISICA']
    sessions_id = {'MATEMATICAS': 165966, 'EX.ORAL  Y ESCRITA': 165965, 'QUIMICA': 165964, 'TICS': 165963, 'FISICA': 165962, 'BIOLOGIA': 165961}
    token = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJjbGFzc29ubGl2ZSIsImRhdGEiOiJ7XCJlbWFpbFwiOlwiaWRtYS5jbGFzc29ubGl2ZUBpZG1hLmNsXCIsXCJpcFwiOlwiMTkyLjE2OC44LjI0OVwifSJ9.B2JvddO1RyMKBLCH7aVctr-CXqGSQS57bCzOifgv4tY'
    

    list_response = []
    if request.method == 'POST':
        datas = request.body
        datas = json.loads(datas.decode('utf-8'))
        print(datas['className'])
        sessionid = sessions_id.get(datas['className'])
        print(sessionid)
        for student in datas['students']:

            # response = requests.put(f"https://www.apiclassonlive.com/api/v1/{token}/particular/{sessionid}/addstudent", params=student)
            # response_code = response.status_code
            # print(response_code)

            if len(student['name']) > 10:
                response_code = 200
                list_response.append([student["email"], response_code])
            else:
                response_code = 403
                list_response.append([student["email"], response_code])


        # print(list_response)
        return HttpResponse(json.dumps(list_response))