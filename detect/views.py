# coding=utf-8
import simplejson
import requests

from django.shortcuts import render
from django.http import JsonResponse

from face.settings import api_key, api_secret
from detect.models import *

# Create your views here.

api_url = "https://api-cn.faceplusplus.com/facepp/v3/detect"


def render_main_page(request):
    return render(request, template_name="index.html")


def render_detect_page(request):
    return render(request, template_name="pricing.html")


def request_detect(file_path):
    file = {"image_file": open(file_path, "rb")}
    info = {"api_key": api_key, "api_secret": api_secret,
            "return_attributes": "gender,age,smiling,headpose,facequality,blur,eyestatus,emotion,ethnicity"}
    r = requests.post(api_url, data=info, files=file)
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


def detect(request):
    info = {}
    result = {"message": "unknown", "info": info, "issuccess": False}
    if request.user.is_authenticated():
        if request.method != "POST": # todo:决定请求方式
            result["message"] = "method not allowed"
            return JsonResponse(result, status=405)

        else:
            f = request.FILES.get("file")
            new_picture = Picture.objects.create()
            file_path = new_picture.avatar_file_save(f)
            dic = request_detect(file_path)
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

