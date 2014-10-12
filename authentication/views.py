from django.shortcuts import render_to_response, HttpResponse

# Create your views here.

def signIn(request):
    if request.POST:
        return HttpResponse("post")
    else:
        return render_to_response("SignIn.html",{})