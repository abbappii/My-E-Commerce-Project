from distutils.command.build_scripts import first_line_re
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def index(request):
    return render(request,'request_data/index.html')

# def validate(request):
#     if request.method == 'POST':
#         # username = request.POST['user']
#         # password = request.POST['pass']
        
#         username = request.POST.get('user')
#         password = request.POST.get('pass')

#         # both working same 

#     context = {
#         'username':username,
#         'password': password
#     }
#     return render(request,'request_data/validate.html',context)

def validate(request):
   if request.method == 'POST':
         hobbies = request.POST.getlist('hobby[]')
   return render(request, 'request_data/validate.html', {'hobbies':hobbies})   

# def registered(request):
#     data = request.POST.items()
#     # for item in request.POST:
#     #     key = item
#     #     value = request.POST[key]
#     # context = {
#     #     'key':key,
#     #     'value': value
#     # }
#     return render(request,'request_data/registered.html',{'data':data})
from  .models import Registration
def registered(request):
    first_name = request.POST.get('fn')
    last_name = request.POST['ln']
    email = request.POST['email']
    password = request.POST.get('password')

    person = Registration(
        frist_name = first_name,
        last_name = last_name,
        email = email,
        password = password
    )
    person.save()

    context = {
        'person':person
    }

    return render(request,'request_data/registered.html',context)