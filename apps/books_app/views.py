# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import messages
from django.shortcuts import render,redirect
from .models import Books
from .models import Author,userDB,Books,Reviews
# Create your views here.
def index(request):
    return render(request,'books_app/index.html')

def reg_home(request):
    return render(request,'books_app/registration.html')

def register(request):
    if( request.method=='POST'):
        ret_val=userDB.objects.register(request.POST)
        print ret_val
        if ret_val[0]:
            #newusers=userDB.objects.all()
            newusers=ret_val[1]
            request.session['user']={
                'id':newusers.id,
                'first_name':newusers.first_name,
                'last_name':newusers.last_name
            }
            context={
                "users": newusers
            }
            messages.add_message(request,messages.INFO,"Registered successfully!")
            return render(request,'books:books',context)
        else:
            for error in ret_val[1]:
                print error;
                messages.error(request,error)
            return redirect('books:reghome')

    return redirect('books:index')



def login(request):
    if( request.method=='POST'):
        ret_val=userDB.objects.login(request.POST)
        if ret_val[0]:
            print ret_val[1].id
            newusers=ret_val[1]
            #newusers=userDB.objects.get(id=ret_val[1].id)
            request.session['user']={
                'id':newusers.id,
                'first_name':newusers.first_name,
                'last_name':newusers.last_name
            }
            context={
                "users": newusers
            }
            print request.session['user']
            messages.add_message(request,messages.INFO,"Logged in successfully!")
            return redirect('books:books')
        else:
            for error in ret_val[1]:
                print error;
                messages.error(request,error)
            return redirect('books:index')

    return redirect('books:index')

def logout(request):
    request.session.clear()
    #userDB.objects.all.delete()
    return redirect('books:index')

def showAdd(request):
    context={
            "books":Books.objects.all(),
            "authors":Author.objects.all()
        }
    return render(request,'books_app/add.html',context)

def add(request):
    if( request.method=='POST'):
        print request.POST['author']
        ret_val=Books.objects.createBook(request.POST)
    if ret_val[0]:
        return redirect('books:showAdd')
    else:
        for error in ret_val[1]:
            print error;
            messages.error(request,error)
        return redirect('books:showAdd')
        context={
            "books":Books.objects.all(),
            "authors":Author.objects.all()
        }
    return redirect('books:books')

def books(request):
    context={
            "books":Books.objects.all(),
            "authors":Author.objects.all()
        }
    print "in index"
    return render(request,'books_app/books.html',context)

def review(request,id):
    context={
            "books":Books.objects.filter(id=id),
        }
    print "in review"
    return render(request,'books_app/review.html',context)

def update(request,id):
    if( request.method=='POST'):
        ret_val=Reviews.objects.updateReview(request.POST,id)
    if ret_val[0]:
        return redirect('books:books')
    else:
        for error in ret_val[1]:
            print error;
            messages.error(request,error)
        return redirect('books:review')
        context={
            "books":Books.objects.all(),
        }
    return redirect('books:books')

def users(request,id):
    pass

def newbook(request,id):
    if(request.method=="POST"):
        author_id=request.POST['author_id']
        a_id=Author.objects.get(id=int(author_id))
        newBook=Books(title=request.POST['book_title'],author=a_id,category=request.POST['book_category'])
        newBook.save()
    return redirect("/")

def newauthor(request):
    if(request.method=="POST"):
        newAuthor=Author.objects.create(first_name=request.POST['first_name'],last_name=request.POST['last_name'])
    return redirect("/")
