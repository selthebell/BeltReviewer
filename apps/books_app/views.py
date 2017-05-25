# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect
from .models import Books
from .models import Author

# Create your views here.
def index(request):
    context={
            "books":Books.objects.all(),
            "authors":Author.objects.all()
        }
    print "in index"
    print context
    return render(request,'books_app/index.html',context)
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
