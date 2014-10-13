from django.shortcuts import render, HttpResponse

# Create your views here.
def signIn(request):
    return render(request,"SignIn.html",{})

def login(request):
    return render(request,"Login.html",{'NEXT':request.GET.get("next","/")})