import requests
import pprint
import socket
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import http.client
import json
import pandas as pd
import pyodbc 
from urllib.parse import urlparse, parse_qs

@csrf_exempt
def webhook(request):
    # Nombre de sesiones ['TICS','MATEMATICAS','EX.ORAL  Y ESCRITA','BIOLOGIA','QUIMICA','FISICA']
    sessions_id = {'MATEMATICAS': 165966, 'EX.  ORAL Y ESCRITA': 165965, 'QUIMICA': 165964, 'TICS': 165963, 'FISICA': 165962, 'BIOLOGIA': 165961, 'GENERO': 173272}
    # token_oficina 
    token = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJjbGFzc29ubGl2ZSIsImRhdGEiOiJ7XCJlbWFpbFwiOlwiaWRtYS5jbGFzc29ubGl2ZUBpZG1hLmNsXCIsXCJpcFwiOlwiMjAwLjU0LjM2LjIyNVwifSJ9.UdfJWxV05uzFxILwNCLF4eFj8jIVxfP7MfB417gZDIw'

    list_response = []
    if request.method == 'POST':
        datas = request.body
        datas = json.loads(datas.decode('utf-8'))
        sessionid = sessions_id.get(datas['className'])
        
        for student in datas['students']:
            student["contentId"] = sessionid
            response = requests.post(f"https://www.apiclassonlive.com/api/v1/{token}/content/student", json=student)
            response_text = response.json()
            response_code = response.status_code
            if response_code == 200:
                if response_text['isNewUser'] == True:
                    list_response.append([student["email"], response_code])
                else:
                    list_response.append([student["email"], response_code])
            else:
                list_response.append([student["email"], response_code])
       
        return HttpResponse(json.dumps(list_response))

@csrf_exempt
def class_progress(request):
    sessions_id = {'MATEMATICAS': 165966, 'EX.  ORAL Y ESCRITA': 165965, 'QUIMICA': 165964, 'TICS': 165963, 'FISICA': 165962, 'BIOLOGIA': 165961, 'GENERO': 173272}
    token = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJjbGFzc29ubGl2ZSIsImRhdGEiOiJ7XCJlbWFpbFwiOlwiaWRtYS5jbGFzc29ubGl2ZUBpZG1hLmNsXCIsXCJpcFwiOlwiMjAwLjU0LjM2LjIyNVwifSJ9.UdfJWxV05uzFxILwNCLF4eFj8jIVxfP7MfB417gZDIw'

    if request.method == 'POST':
        datas = request.body
        datas = json.loads(datas.decode('utf-8'))
        content_id = sessions_id.get(datas.upper())
        
        page_number = 0
        list_progress_students = []
        end = True
        while end:
            response_text = requests.get(f"https://www.apiclassonlive.com/api/v1/{token}/student/getstatsfromcontent/{content_id}/{page_number}").json() 
            page_number+=1
            if len(response_text['stats']) > 0:
                for text in response_text['stats']:
                    exam_list = []
                    for exam in text['detail']:
                        if exam['examTries'] != None:
                            exam_list.append(exam['percent'])
                    list_progress_students.append([text['general']['name'],text['general']['email'], text['general']['totalTime'], text['general']['totalPercent'], text['general']['registerDate'], exam_list[0], exam_list[1], exam_list[2]])
            else:
                end = False  

        return HttpResponse(json.dumps(list_progress_students))
    

import re
@csrf_exempt
def query(request):
    if request.method == 'GET':
        try:
            query = request.GET.get('query', None)
            print(query)
            server = '10.0.1.252' 
            database = 'idma_net' 
            username = 'guestidma' 
            password = 'Q@:aKBhpg}' 
            cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
            cursor = cnxn.cursor()
            
            
            cursor.execute(f"""{query}""") 
            row = cursor.fetchall() 
            results = [tuple(row) for row in row]
            json_string = json.dumps(results, default=str)
        except Exception as e:
            print("Ocurrió un error al consultar: ", e)
        finally:
            cnxn.close()

        return HttpResponse(json_string)



# @csrf_exempt
# def coevaluacion(request):
#     if request.method == 'POST':
#         datas = request.body
#         datas = json.loads(datas.decode('utf-8'))
#         df = pd.DataFrame(datas[1:], columns = datas[0])
#         df= df.replace(',','.' , regex=True)
#         df = df.astype({'Cantidad Alumnos':'int','Cantidad que Contestaron':'int'})
#         df = df.astype({'63':'float64','64':'float64','65':'float64','66':'float64','67':'float64','68':'float64','69':'float64','promedio 1':'float64','70':'float64','71':'float64','72':'float64','73':'float64','74':'float64','75':'float64','76':'float64','promedio 2':'float64','77':'float64','78':'float64','Promedio Final':'float64'})
#         print(df)
#         df = df.groupby(['Nombre','Nombre Ramo']).aggregate({
#             'Ramo_Seccion': 'last',
#             'Correo':'last',
#             'Cantidad Alumnos':'sum',
#             'Cantidad que Contestaron':'sum',   
#             '63':'mean',
#             '64':'mean',
#             '65':'mean',
#             '66':'mean',
#             '67':'mean',
#             '68':'mean',
#             '69':'mean',
#             'promedio 1':'mean',
#             '70':'mean',
#             '71':'mean',
#             '72':'mean',
#             '73':'mean',
#             '74':'mean',
#             '75':'mean',
#             '76':'mean',
#             'promedio 2':'mean',
#             '77':'mean',
#             '78':'mean',
#             'Promedio Final':'mean'
#             })
#         print(df)
#         df.to_excel('agrupado.xlsx')
#         dict = df.to_numpy().tolist()
#         headers = df.columns.tolist()
#         dict[:0] = headers
#         return HttpResponse(json.dumps(dict))