# coding=utf-8
import simplejson
import requests
import json

from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from face.settings import api_key, api_secret
from face.Error import *
from detect.models import *

# Create your views here.

api_url = "https://api-cn.faceplusplus.com/facepp/v3/detect"


@login_required(login_url="/")
def render_main_page(request):
    return render(request, template_name="index.html")


@login_required(login_url="/")
def render_detect_page(request):
    return render(request, template_name="identify.html")


@login_required(login_url="/")
def render_compare_page(request):
    return render(request, template_name="compare.html")


def request_detect(img_url=None, file_path=None):
    info = {"api_key": api_key, "api_secret": api_secret,
            "return_attributes": "gender,age,smiling,headpose,facequality,blur,eyestatus,emotion,ethnicity"}
    if file_path:
        file = {"image_file": open(file_path, "rb")}
        r = requests.post(api_url, data=info, files=file)
    if img_url:
        info["image_url"] = img_url
        r = requests.post(api_url, data=info)
    return simplejson.loads(r.text)


def select(dict):
    result = ""
    tempList = []
    for key, value in dict.items():
        try:
            if value > tempList[0]:
                tempList[0] = value
                result = key
            else:
                pass
        except Exception:
            tempList.append(value)
            result = key
    return result


@login_required(login_url="/")
def detect(request):
    info = {}
    result = {"message": "unknown", "info": info, "issuccess": False}
    if request.user.is_authenticated():
        if request.method != "POST": # todo:决定请求方式
            result["message"] = "method not allowed"
            return JsonResponse(result, status=405)

        else:
            f = request.FILES.get("myfile")
            if f:
                new_picture = Picture.objects.create()
                file_path = new_picture.pic_file_save(f)
                dic = request_detect(file_path=file_path)
            else:
                form_info = json.loads(request.body.decode())
                img_url = form_info["img_url"]
                if img_url:
                    dic = request_detect(img_url=img_url)
                else:
                    result["message"] = "need more arguments"
                    return JsonResponse(result, status=402)
            faceList = dic["faces"]
            faceDict = faceList[0]
            rectangleDict = faceDict["face_rectangle"]
            AttributeDict = faceDict["attributes"]
            info["position"] = rectangleDict
            info["gender"] = AttributeDict["gender"]["value"]
            info["age"] = AttributeDict["age"]["value"]
            smileThreshold = AttributeDict["smile"]["threshold"]
            smileValue = AttributeDict["smile"]["value"]
            if (smileValue > smileThreshold):
                info["smile"] = True
            else:
                info["smile"] = False
            # todo：人脸姿势、人脸质量（用于人脸比对）
            info["emotion"] = select(AttributeDict["emotion"])
            info["eyestatus"] = select(AttributeDict["eyestatus"])
            ethValue = AttributeDict["ethnicity"]["value"]
            if ethValue == "Asian":
                info["ethnicity"] = "asian"
            elif ethValue == "White":
                info["ethnicity"] = "white"
            else:
                info["ethnicity"] = "black"
            result["issuccess"] = True
            return JsonResponse(result, status=200)
    else:
        result["message"] = u"需要登录"
        return JsonResponse(result, status=403)

