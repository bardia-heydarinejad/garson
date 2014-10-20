from django.shortcuts import render, HttpResponse

# Create your views here.
def home(request):
    msg = request.GET.get("msg")
    return render(request,"index.html",{'msg':msg})