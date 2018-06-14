from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
import json
import CloudJudge.info as info

FrontMessageCode = info.getFrontMessage()

def getFrontMessageCode(request):

    if request.method == "GET":
        return HttpResponse(json.dumps(FrontMessageCode), content_type="application/json")
    else:
        return HttpResponse(status=400)
