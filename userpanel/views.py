from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.
from userpanel.models import UserCollection


@login_required(login_url='/authentication/login/')
def userPanel(request):
    name = ""
    us = UserCollection.objects(userId=request.user.id)
    if len(us) == 1:
        name = us[0].name if us[0].name is not None else ""
    return render(request,"UserPanel.html",{"name":name})