import requests
import pprint
import socket
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import http.client
import json
import pandas as pd

@csrf_exempt
def webhook(request):
    # Nombre de sesiones ['TICS','MATEMATICAS','EX.ORAL  Y ESCRITA','BIOLOGIA','QUIMICA','FISICA']
    sessions_id = {'MATEMATICAS': 165966, 'EX. ORAL Y ESCRITA': 165965, 'QUIMICA': 165964, 'TICS': 165963, 'FISICA': 165962, 'BIOLOGIA': 165961}
    # token_oficina 
    # token = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJjbGFzc29ubGl2ZSIsImRhdGEiOiJ7XCJlbWFpbFwiOlwiaWRtYS5jbGFzc29ubGl2ZUBpZG1hLmNsXCIsXCJpcFwiOlwiMTkyLjE2OC44LjI0OVwifSJ9.B2JvddO1RyMKBLCH7aVctr-CXqGSQS57bCzOifgv4tY'
    # token_casa 
    token = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJjbGFzc29ubGl2ZSIsImRhdGEiOiJ7XCJlbWFpbFwiOlwiaWRtYS5jbGFzc29ubGl2ZUBpZG1hLmNsXCIsXCJpcFwiOlwiMTkwLjExNC4zMy4xMDFcIn0ifQ.ixEL3i_LTyrkbyXeat0ENxNLeoVyFu6dxs7_a5HYpCk'

    list_response = []
    if request.method == 'POST':
        datas = request.body
        datas = json.loads(datas.decode('utf-8'))
        sessionid = sessions_id.get(datas['className'])

        for student in datas['students'][:70]:
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
    sessions_id = {'MATEMATICAS': 165966, 'EX. ORAL Y ESCRITA': 165965, 'QUIMICA': 165964, 'TICS': 165963, 'FISICA': 165962, 'BIOLOGIA': 165961}
    # token_oficina 
    # token = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJjbGFzc29ubGl2ZSIsImRhdGEiOiJ7XCJlbWFpbFwiOlwiaWRtYS5jbGFzc29ubGl2ZUBpZG1hLmNsXCIsXCJpcFwiOlwiMTkyLjE2OC44LjI0OVwifSJ9.B2JvddO1RyMKBLCH7aVctr-CXqGSQS57bCzOifgv4tY'
    # token_casa 
    token = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJjbGFzc29ubGl2ZSIsImRhdGEiOiJ7XCJlbWFpbFwiOlwiaWRtYS5jbGFzc29ubGl2ZUBpZG1hLmNsXCIsXCJpcFwiOlwiMTkwLjExNC4zMy4xMDFcIn0ifQ.ixEL3i_LTyrkbyXeat0ENxNLeoVyFu6dxs7_a5HYpCk'

    list_response = []
    if request.method == 'POST':
        datas = request.body
        datas = json.loads(datas.decode('utf-8'))
        content_id = sessions_id.get(datas.upper())
        page_number = 1
        list_progress_students = []

        end = True
        while end:
            response = requests.get(f"https://www.apiclassonlive.com/api/v1/{token}/student/getstatsfromcontent/{content_id}/{page_number}")
            response_text = response.json() 
            page_number+=1
            if len(response_text['stats']) > 0:
                for text in response_text['stats']:
                    exam_list = []
                    key_list = list(text['detail'].keys())
                    val_list = list(text['detail'].values())

                    position = val_list.index(100)
                    print(key_list[position])

                    # for exam in text['detail']:s
                    #     if exam['examTries'] != None:
                    #         exam_list.append(exam['percent'])

                    list_progress_students.append(["today" , text['general']['name'],text['general']['email'], text['general']['totalTime'], text['general']['totalPercent'], text['general']['registerDate'], exam_list[0], exam_list[1], exam_list[2]])
            else:
                end = False  

# Fecha	Nombre	Email	Tiempo Conectado (min)	 Completado	Fecha de Registro	EVA 1	EVA 2	EVA 3
# 15-02-2022	martina.bustamante	martina.bustamante@idma.cl	0	0	14-02-2022			
        print(list_progress_students)
        return HttpResponse(json.dumps(list_response))


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