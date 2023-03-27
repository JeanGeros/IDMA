import requests
import pprint
import socket
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import http.client
import json
import pandas as pd
import pyodbc
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.support.ui import Select

@csrf_exempt
def webhook(request):
    # Nombre de sesiones ['TICS','MATEMATICAS','EX.ORAL  Y ESCRITA','BIOLOGIA','QUIMICA','FISICA']
    sessions_id = {'MATEMATICAS': 165966, 'EX.  ORAL Y ESCRITA': 165965, 'QUIMICA': 165964, 'TICS': 165963, 'FISICA': 165962, 'BIOLOGIA': 165961, 'GENERO': 173272}
    # token_oficina 
    token = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJjbGFzc29ubGl2ZSIsImRhdGEiOiJ7XCJlbWFpbFwiOlwiaWRtYS5jbGFzc29ubGl2ZUBpZG1hLmNsXCIsXCJpcFwiOlwiMTkwLjExNC4zNS4xNlwifSJ9.s55cKx9dGF4yI3P5Le0KevDLX5GEVVruyKbU5uGRH3M'

    list_response = []
    if request.method == 'POST':
        datas = request.body
        datas = json.loads(datas.decode('utf-8'))
        sessionid = sessions_id.get(datas['className'])
        
        for student in datas['students'][:30]:
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
    token = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJjbGFzc29ubGl2ZSIsImRhdGEiOiJ7XCJlbWFpbFwiOlwiaWRtYS5jbGFzc29ubGl2ZUBpZG1hLmNsXCIsXCJpcFwiOlwiMTkwLjExNC4zNS4xNlwifSJ9.s55cKx9dGF4yI3P5Le0KevDLX5GEVVruyKbU5uGRH3M'

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
    

@csrf_exempt
def query(request):
    if request.method == 'GET':
        try:
            query = request.GET.get('query', None)
            print("----------------------------------------")
            print(query)
            print("----------------------------------------")
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


@csrf_exempt
def course_creation(request):
    token = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJjbGFzc29ubGl2ZSIsImRhdGEiOiJ7XCJlbWFpbFwiOlwiaWRtYS5jbGFzc29ubGl2ZUBpZG1hLmNsXCIsXCJpcFwiOlwiMjAwLjU0LjM2LjIyNVwifSJ9.UdfJWxV05uzFxILwNCLF4eFj8jIVxfP7MfB417gZDIw'
    if request.method == 'POST':
        datas = request.body
        courses = json.loads(datas.decode('utf-8'))
        json_create = {'title': "", 'type': "Temas"}
        list_response = []
        for course in courses:
            print(course)
            json_create["title"] = course
            response = requests.post(f"https://www.apiclassonlive.com/api/v1/{token}/content", json=json_create)
            response_text = response.json()
            response_code = response.status_code
            print(response_text)
            if response_code == 200:
                list_response.append(response_text["contentId"])
            else:
                list_response.append("Error")
        return HttpResponse(json.dumps(list_response))

@csrf_exempt
def assign_teachers(request):
    token = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJjbGFzc29ubGl2ZSIsImRhdGEiOiJ7XCJlbWFpbFwiOlwiaWRtYS5jbGFzc29ubGl2ZUBpZG1hLmNsXCIsXCJpcFwiOlwiMjAwLjU0LjM2LjIyNVwifSJ9.UdfJWxV05uzFxILwNCLF4eFj8jIVxfP7MfB417gZDIw'
    list_teachers = {'Agricultura I': 'agricultura@idma.cl',
                     'Agricultura III': 'agricultura2@idma.cl',
                     'Paisajismo I': 'paisajismo@idma.cl',
                     'Paisajismo III': 'paisajismo2@idma.cl',
                     'Construcción III': 'construccion@idma.cl',
                     'Construcción I': 'construccion@idma.cl',
                     'Medio Ambiente I': 'ambiente@idma.cl',
                     'Medio Ambiente III': 'ambiente2@idma.cl',
                     'Veterinaria I': 'veterinaria@idma.cl',
                     'Veterinaria III': 'veterinaria2@idma.cl',
                     'Energias I': 'energias@idma.cl',
                     'Energías III': 'energias2@idma.cl',
                     'Ecoturismo I': 'turismo@idma.cl',
                     'Ecoturismo III': 'turismo2@idma.cl',
                     'Manejo Areas I': 'turismo@idma.cl',
                     'Manejo Areas III': 'turismo2@idma.cl',
                     'Salud Y Terapias I': 'salud@idma.cl',
                     'Salud Y Terapias III': 'salud2@idma.cl',
                     'Transversal': 'a.transversales@idma.cl'}


    if request.method == 'POST':
        datas = request.body
        courses = json.loads(datas.decode('utf-8'))
        json_create = {'title': "", 'type': "Temas"}
        list_response = []
        for course in courses:

            sessionid = sessions_id.get(datas['className'])


            print(course)
            json_create["title"] = course
            response = requests.post(f"https://www.apiclassonlive.com/api/v1/{token}/content", json=json_create)
            response_text = response.json()
            response_code = response.status_code
            print(response_text)
            if response_code == 200:
                list_response.append(response_text["contentId"])
            else:
                list_response.append("Error")
        return HttpResponse(json.dumps(list_response))

@csrf_exempt
def assign_automatic(request):
    if request.method == 'GET':
        teacher = request.GET.get('teacher', None)
        course = request.GET.get('course', None)
        course = json.loads(course)

        print("----------------------------------------")
        print(teacher)
        print(course)
        print("----------------------------------------")

        driver = webdriver.Chrome('./chromedriver')
        driver.implicitly_wait(10)
        # INICIO DE SESION
        driver.get(f"https://www.classonlive.com/zona-privada/Editor-Formacion?type=Drip&cursoId={course}")
        time.sleep(2)
        driver.find_element(By.XPATH, "/html/body/section/div[1]/div/form/div[1]/button").click()
        driver.find_element(By.XPATH, "/html/body/section/div[1]/div/form/div[2]/div[1]/input").send_keys("idma.classonlive@idma.cl")
        driver.find_element(By.XPATH, "/html/body/section/div[1]/div/form/div[2]/div[2]/input").send_keys("idmaclassonlive")
        driver.find_element(By.XPATH, "/html/body/section/div[1]/div/form/div[2]/div[4]/button").click()
        time.sleep(5)

        for c in course:
            auto_assign_teacher(driver, c, teacher)

        return HttpResponse("uwu")


@csrf_exempt
def assign_creater(request):
    if request.method == 'GET':
        start = request.GET.get('start', None)
        teacher = request.GET.get('teacher', None)
        courses = json.loads(teacher)

        start = int(start)

        print("----------------------------------------")
        print(start)
        print(end)
        print(teacher)
        print("----------------------------------------")


        driver = webdriver.Chrome('./chromedriver')
        driver.implicitly_wait(10)
        # INICIO DE SESION
        driver.get(f"https://www.classonlive.com/zona-privada/Cursos-que-Imparto")
        time.sleep(2)
        driver.find_element(By.XPATH, "/html/body/section/div[1]/div/form/div[1]/button").click()
        driver.find_element(By.XPATH, "/html/body/section/div[1]/div/form/div[2]/div[1]/input").send_keys("idma.classonlive@idma.cl")
        driver.find_element(By.XPATH, "/html/body/section/div[1]/div/form/div[2]/div[2]/input").send_keys("idmaclassonlive")
        driver.find_element(By.XPATH, "/html/body/section/div[1]/div/form/div[2]/div[4]/button").click()
        time.sleep(8)
        driver.get(f"https://www.classonlive.com/zona-privada/Cursos-que-Imparto")
        time.sleep(2)

        while start > int(end)-1:
            print(start)
            driver.execute_script("window.scrollBy(0,document.body.scrollHeight)")
            time.sleep(1)


            driver.find_element(By.XPATH, f"/html/body/div[5]/div[4]/div[1]/div[3]/section/div/div[2]/div/table/tbody/tr[{start}]/td[9]/div/button").click()
            time.sleep(1)
            driver.find_element(By.XPATH, f"/html/body/div[5]/div[4]/div[1]/div[3]/section/div/div[2]/div/table/tbody/tr[{start}]/td[9]/div/ul/li[13]/a").click()
            time.sleep(2)
            select_driver = Select(driver.find_element(By.XPATH, f"/html/body/div[5]/div[4]/div[22]/div/div/div[2]/div/div/div/div/select"))
            select_driver.select_by_visible_text(f"{teacher}")
            time.sleep(1)
            driver.find_element(By.XPATH, f"/html/body/div[5]/div[4]/div[22]/div/div/div[3]/div[2]/button[1]").click()
            time.sleep(12)
            start -= 1

        return HttpResponse("uwu")


def auto_assign_teacher(driver, course, teacher):
      # MODIFICACION DE CURSO

    driver.get(f"https://www.classonlive.com/zona-privada/Editor-Formacion?type=Drip&cursoId={course}")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[5]/div[4]/div[2]/div/div[2]/div[2]"))
    ).click()

    # MODIFICACANDO PARAMETROS
    driver.find_element(By.XPATH,"/html/body/div[5]/div[4]/div[3]/div[1]/div/div[2]/div[2]/div[1]/div[2]/div/div/div[3]/div[2]").send_keys(".")
    driver.find_element(By.XPATH,"/html/body/div[5]/div[4]/div[3]/div[1]/div/div[2]/div[2]/div[2]/div[2]/div/div/div[3]/div[2]").send_keys(".")
    driver.find_element(By.XPATH,"/html/body/div[5]/div[4]/div[3]/div[1]/div/div[2]/div[2]/div[3]/div[2]/div/div/div[3]/div[2]").send_keys(".")
    time.sleep(1)
    # ASIGNAMOS AL DOCENTE

    driver.find_element(By.XPATH,"/html/body/div[5]/div[4]/div[3]/div[1]/div/div[2]/div[2]/div[4]/div[2]/div").click()
    driver.find_element(By.XPATH,"/html/body/div[5]/div[4]/div[3]/div[1]/div/div[2]/div[2]/div[4]/div[2]/div/ul/li/input").send_keys(f"{teacher}")
    time.sleep(1)
    driver.find_element(By.XPATH,"/html/body/div[5]/div[4]/div[3]/div[1]/div/div[2]/div[2]/div[4]/div[2]/div/ul/li/input").send_keys(Keys.ENTER)

    driver.find_element(By.XPATH,"/html/body/div[5]/div[4]/div[3]/div[1]/div/div[15]/button").click()
    time.sleep(10)



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