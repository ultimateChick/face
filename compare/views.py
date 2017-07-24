# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from face.settings import api_secret, api_key
from face.Error import *
from detect.models import Picture

import requests
import simplejson

api_url = "https://api-cn.faceplusplus.com/facepp/v3/compare"


def render_compare_page(request):
    return render(request, template_name="compare.html")


def compare_request(img_url1=None, file_path1=None, img_url2=None, file_path2=None):
    info = {"api_key": api_key, "api_secret": api_secret}
    if img_url1 and img_url2:
        info["image_url1"] = img_url1
        info["image_url2"] = img_url2
        r = requests.post(api_url, data=info)
    if file_path1 and file_path2:
        file = {"image_file1": open(file_path1, "rb"), "image_file2": open(file_path2, "rb")}
        r = requests.post(api_url, data=info, files=file)
    return simplejson.loads(r.text)


def possibility(thresholds, confidence):
    e5 = thresholds["1e-5"]
    if confidence >= e5:
        return "high"
    e4 = thresholds["1e-4"]
    if confidence >= e4:
        return "mediun"
    e3 = thresholds["1e-3"]
    if confidence >= e3:
        return "low"
    return "no"


@login_required(login_url="/")
def compare(request):
    result = {"message": "unknown", "isscuess": False}

    if request.method != "POST":
        result["message"] = "method not allowed"
        return JsonResponse(result, status=405)

    else:
        f1 = request.FILES.get("file1")
        f2 = request.FILES.get("file2")
        if f1 and f2:
            new_pic1 = Picture.objects.create()
            new_pic2 = Picture.objects.create()
            file_path1 = new_pic1.pic_file_save(f1)
            file_path2 = new_pic2.pic_file_save(f2)
            dic = compare_request(file_path1=file_path1, file_path2=file_path2)
        else:
            # form_info = simplejson.loads(request.body.decode())
            img_url1 = request.POST.get("img_url1")
            img_url2 = request.POST.get("img_url2")
            if img_url1 and img_url2:
                dic = compare_request(img_url1=img_url1, img_url2=img_url2)
            else:
                result["message"] = "need more arguments"
                return JsonResponse(result, status=402)
        try:
            confidence = dic["confidence"]  # 置信度
        except Exception:
            err_message = dic["error_message"]
            result["message"] = err_message
            return JsonResponse(result, status=402)
        thresholds = dic["thresholds"]
        p = possibility(thresholds, confidence)
        result["possibility"] = p
        result["isscuess"] = True
        return JsonResponse(result, status=200)



