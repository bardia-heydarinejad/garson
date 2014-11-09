from django.shortcuts import render
from django.contrib.auth.models import User

# Create your views here.
def home(request):
    msg = request.GET.get("msg")
    return render(request,"index.html",{'msg':msg,'user_count':len(User.objects.all())})