from django.http import HttpResponse
from django.shortcuts import render,redirect
from .forms import FilesForm
from .models import Files, User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
import os,shutil
from django.db.models import Q,F

@login_required(login_url='signin')
def addfile(request):
    if request.method=="POST":
        form=FilesForm(request.POST,request.FILES)
        form.instance.user=request.user
        form.instance.author_id=request.user.id
        if form.is_valid():
            form.save()
            return redirect(home)
    else:
        form=FilesForm
    return render(request,"form.html",{"form":form})

def home(request):
    if(request.user.is_authenticated):
        my_files=Files.objects.filter(user=request.user,author_id=request.user.id)
        imported_files=Files.objects.filter(~Q(author_id=request.user.id),user=request.user)
        return render(request,"home.html",{"files":my_files,"imports":imported_files})
    else:
        return redirect(signin)

# def delete_file(request,file_id):
#     file=Files.objects.get(id=file_id)
#     if(file):
#         if(file.author_id==request.user.id):
#             if(os.path.exists("uploads/"+file.file.name)):
#                 os.remove("uploads/"+file.file.name)
#             file.delete()
#             return redirect(home)
#         else:
#             file.delete()
#             return redirect(home)
#     else:
#         return HttpResponse(f"File with id: {file_id} not found!!")

def delete_file(request,file_id):
    file=Files.objects.get(id=file_id)
    if(file):
        if(file.author_id==request.user.id):
            if(os.path.exists("uploads/"+file.file.name)):
                os.remove("uploads/"+file.file.name)
            file.delete()
            shared_files=Files.objects.filter(~Q(user=request.user),author_id=request.user.id)
            if(shared_files):
                for shared_f in shared_files:
                    shared_f.delete()
            return redirect(home)
        else:
            file.delete()
            return redirect(home)
    else:
        return HttpResponse(f"File with id: {file_id} not found!!")

def pdf_view(request,file_name):
    if(file_name[-3:]=="pdf"):
        with open("uploads/"+file_name, 'rb') as pdf:
            response = HttpResponse(pdf.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'inline;filename={file_name.split("/")[-1]}'
            return response
    elif(file_name[-3:]=="ocx"):
        with open("uploads/"+file_name,'rb') as doc:
            response = HttpResponse(doc.read(), content_type='application/ms-word')
            response['Content-Disposition'] = f'inline;filename={file_name.split("/")[-1]}'
            return response
    else:
        with open("uploads/"+file_name,'rb') as doc:
            response = HttpResponse(doc.read(), content_type='application/ms-word')
            response['Content-Disposition'] = f'inline;filename={file_name.split("/")[-1]}'
            return response

def signup(request):
    if(request.user.is_authenticated):
        return redirect(home)
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(request,username=username, password=password)
            login(request, user)
            return redirect(home)
        else:
            form = UserCreationForm()
            return render(request, "signup.html", {"form": form,"msg":"Invalid Details has been given"})
    else:
        form = UserCreationForm()
        return render(request, "signup.html", {"form": form})

def signin(request):
    if(request.user.is_authenticated):
        return redirect(home)
    if request.method == "POST":
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect(home)
        else:
            form=AuthenticationForm(request.POST)
            return render(request, "login.html", {"form": form,"msg":"Invalid Details has been given"})
    else:
        form=AuthenticationForm(request.POST)
        return render(request,"login.html",{"form":form})

def signout(request):
    logout(request)
    return redirect(signin)

def view_users(request):
    if(request.GET.get("search") is not None):
            q=request.GET.get("search")
            filtered_users=User.objects.filter(username__icontains=q).exclude(id=request.user.id)
            if(len(filtered_users)>0):
                users=User.objects.exclude(id=request.user.id).all
                return render(request,"users.html",{"filteredusers":filtered_users,"users":users})
            else:
                users=User.objects.exclude(id=request.user.id).all
                return render(request,"users.html",{"users":users,"msg":f"No results found for your search query {request.GET.get('search')}"})
    else:
        users=User.objects.exclude(id=request.user.id).all
        return render(request,"users.html",{"users":users})
def all_files(request):
    files=Files.objects.filter(author_id=F("user_id"))
    return render(request,"all_files.html",{"files":files})


def user_profile(request,user_id):
    files=Files.objects.filter(user=user_id,author_id=user_id)
    return render(request,"user_profile.html",{"files":files})

def import_file(request,file_id):
    file=Files.objects.get(id=file_id)
    print(file.file)
    form=Files(user=request.user,name=file.name,file=file.file,author_id=file.user.id)
    form.save()
    return redirect(home)