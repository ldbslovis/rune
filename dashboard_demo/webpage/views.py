from django.shortcuts import render, redirect
from django.http import HttpResponse
# Create your views here.

import sys
import requests
sys.path.insert(0, '../runebook')

from runebook import *

def index(request):
    return render(request, 'login.html', {})
    #return HttpResponse("Hello, world. You're at the polls index.")

def loginProc(request):
    cond = {"email": request.POST["email"], "password": request.POST["password"]}

    result = requests.post("http://175.126.112.130:8888/getAuth", json=cond) 
    if result is None or result is ():
        return redirect('index')

    userInfo = result.json()
    
    print(userInfo)

    if userInfo is () or userInfo is None:
        return redirect('index')

    request.session["userinfo"] = userInfo
    return redirect('project_list')

def projectList(request):
    userInfo = request.session["userinfo"]
    cond = {"user_id": userInfo[0]}
    ret = requests.post("http://175.126.112.130:8888/getProjectList", json=cond)
    print(ret)
    return render(request, 'project_list.html', {"list": ret.json(), "user": userInfo})

def addProjectProc(request):
    userInfo = request.session["userinfo"]
    if userInfo is () or userInfo is None:
        return redirect('index')

    projectName = request.POST["project_name"]
    cond = {"user_id": userInfo[0], "project_name": projectName}

    if str(projectName).strip() == "":
        return redirect('project_list')

    ret = requests.post("http://175.126.112.130:8888/addProject", json=cond)
    
    return redirect('project_list')


def codeList(request):
    projectId = request.GET["project_id"]

    userInfo = request.session["userinfo"]
    if userInfo is () or userInfo is None:
        return redirect('index')

    cond = {"project_id": projectId}
    print(cond)
    ret = requests.post("http://175.126.112.130:8888/getFunctionList", json=cond)
    print(ret)
    return render(request, 'code_list.html', {"list": ret.json(), "user": request.session["userinfo"], "project_id": projectId})    

def setCode(request):
    userInfo = request.session["userinfo"]

    codeData = None
    if "code_id" in  request.GET.keys():
        cond = {"code_id": request.GET["code_id"]}
        codeData = requests.post("http://175.126.112.130:8888/getFunction", json=cond)

    return render(request, 'code_form.html', {"code_data" : codeData.json(), "project_id": request.GET["project_id"]})

def setCodeProc(request):
    userInfo = request.session["userinfo"]

    codeName = request.POST["code_name"]
    codeArea = str(request.POST["code_area"])
    projectId = request.POST["project_id"]

    codeId = None

    if "id" in request.POST.keys():
        codeId = request.POST["id"]

    print(codeId)
    codeData = None

    codeObject = RuneCode(projectId, codeName, codeArea, None, codeId)
    #codeObject = RuneCode(projectId, codeArea, None, codeId)

    if codeId != None:
        cond = {"code_id": codeId, "project_id": projectId, "code_name": codeName, "code_area": codeArea}
        ret = requests.post("http://175.126.112.130:8888/updateFunction", json=cond)
    else:
        cond = {"project_id": projectId, "code_name": codeName, "code_area": codeArea}
        ret = requests.post("http://175.126.112.130:8888/addFunction", json=cond)

    return render(request, 'code_form_proc.html', {"ret": ret})
