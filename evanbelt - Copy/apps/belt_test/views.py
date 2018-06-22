from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from  datetime import datetime
import bcrypt
import re
from django.db.models import Q
from .models import *

# Create your views here.
def index(request):
  return render(request, "pages/index.html")

def check_password(request, username, password):
      u = User.objects.filter(username=username).first()
      if u == None:
          messages.add_message(request, messages.ERROR, "Not registered!")
          return 1
      hashed = u.password
      if bcrypt.hashpw(password.encode("utf-8"), hashed.encode("utf-8")) == hashed.encode("utf-8"):
        print ("It matches")
        return u
      else:
        messages.add_message(request, messages.ERROR, "Password doesnt match!")
        print ("no match")
        return 2

def login(request):
    error = None
    username = request.POST['username']
    password = request.POST['password']
    if len(username) < 1:
       error="error"
       messages.add_message(request, messages.ERROR, 'username has to be at least 3 characters! ')
    if len(password) < 8:
        messages.add_message(request, messages.ERROR, 'Password has to be at least 8 characters! ')
        error="error"
    if error == "error":
        return redirect("/login")
        #return render(request, 'dashboard/signin.html')
    user = check_password(request=request, username=username, password=password)
    if user == 1:
        return redirect("/login")
    if user == 2:
        return redirect("/login")
    if user != None:
        request.session['user_id'] = user.id
        request.session['username'] = user.username
        return redirect("/show_dashboard")

def show_dashboard(request):
    user = User.objects.get(id=request.session['user_id'])
    ww = Wishlist.objects.all()
    mywishlist = []
    otherwishlist = []
    for w in ww:
        for u in w.users.all():
            if u == user:
                mywishlist.append(w)
            else:
                otherwishlist.append(w)
    #mywishlist = user.wishlist_set.all()
    context = {
      "mywishlist": mywishlist,
      "otherwishlist": otherwishlist,
      "allwishlist": ww
    }
    return render(request, 'belt_test/dashboard.html', context)

def registration(request):
        error = None
        name = request.POST['name']
        username = request.POST['username']
        datehired = request.POST['datehired']
        password = request.POST['password']
        if len(username) < 3:
           error="error"
           messages.add_message(request, messages.ERROR, 'username has to be at least 3 characters! ')
        if len(password) < 8:
           messages.add_message(request, messages.ERROR, 'Password has to be at least 8 characters! ')
           error="error"
        confirm_password = request.POST['password_confirm']
        if password != confirm_password:
           error="error"
           messages.add_message(request, messages.ERROR, 'Password and Confirm Password do not match! ')
        if len(name) < 3:
           error="error"
           messages.add_message(request, messages.ERROR, 'name has to be at least 3 letters! ')
        if error == None:
            if User.objects.filter(username=username).first():
                context = {
                    "category": "register"
                }
                messages.add_message(request, messages.ERROR, 'user exists! Please log in! ')
                return render(request, 'belt_test/index.html', context)
            passwd_encoded = password.encode('utf-8')
            hashed = bcrypt.hashpw(passwd_encoded, bcrypt.gensalt())
            user = User.objects.create(name=name, username=username, password=hashed, date=datehired)
            # print "User objects after create"
            request.session['user_id'] = user.id
            request.session['username'] = user.name
            return redirect("/show_dashboard")
        else:
            context = {
                "category": "register"
            }
            return render(request, 'belt_test/index.html', context)

def create_item(request):
    return render(request, 'belt_test/create_item.html')

def add(request, id):
    u =  User.objects.get(id=request.session['user_id'])
    w = Wishlist.objects.get(id=id)
    w.users.add(u)
    return redirect("/show_dashboard")

def delete(request, id):
  w = Wishlist.objects.get(id=id)
  w.delete()
  return redirect("/show_dashboard")

def remove(request, id):
  user = User.objects.get(id=request.session['user'])
  w = Wishlist.objects.get(id=id)
  for e in w.users:
      if e.name == user.name:
          del e
  for p in pp:
      p.delete()
  return redirect("/show_dashboard")

def create(request):
    if len( request.POST['itemname']) < 3:
       error="error"
       messages.add_message(request, messages.ERROR, 'item name has to be at least 3 letters! ')
       return redirect("/create_item")
    else:
       creator =  User.objects.get(id=request.session['user_id'])
       user = Wishlist.objects.create(name=request.POST['itemname'], creator=creator, created_at=datetime.date.today)
       return redirect("/show_dashboard")


def show_item(request, id):
    Context  = {
        "item": Wishlist.objects.get(id=id)
    }
    return render(request, 'belt_test/show_item.html', Context)

def logoff(request):
    try:
        del request.session['user_id']
        del request.session['username']
    except KeyError:
        pass
    return redirect('/')
