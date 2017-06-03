# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import bcrypt
from django.db import models
import re
EMAIL_REGEX=re.compile(r"(^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")


# Create your models here.

class userDBManager(models.Manager):
      def login(self, postData):
          errors=[]
          ret_user=userDB.objects.filter(email=postData['email'])
          if ret_user:
              userFound=userDB.objects.get(email=postData['email'])
              password=postData['password'].encode()
              # Hash a password for the first time, with a randomly-generated salt
              hashed = bcrypt.hashpw(password, bcrypt.gensalt())
                # Check that a unhashed password matches one that has previously been
                #   hashed
              if bcrypt.hashpw(password, hashed) == hashed:
              #if (postData['password']==userFound.password):
                  print userFound
                  print "Running a login function!"
                  return(True,userFound)
              else:
                  errors.append("Couldnt login")
                  return(False,errors)
          else:
              errors.append("Couldnt login")
              return(False,errors)
         # print "If successful login occurs, maybe return {'theuser':user} where user is a user object?"
         # print "If unsuccessful, maybe return { 'errors':['Login unsuccessful'] }"
      def register(self, postData):
          errors=[]
          print postData
          if(len(postData['first_name'])<=2 or len(postData['last_name'])<=2):
              print "Name is not entered"
              errors.append("Name has to be atleast 2characters!")
          if( (len(postData['email'])<=0) or (len(postData['email'])>120) or (not EMAIL_REGEX.match(postData['email'])) ):
              print "email has to entered as test@tesmail.com"
              errors.append("Please enter email ")
          if(len(postData['password'])<=8):
              print "password less than 8characters"
              errors.append("Password needs to be 8 characters long")
          if(postData['password']<>postData['confirm_pwd']):
              print "both passwords do not match"
              errors.append("Please confirm password")
          if errors:
              print "not created"
              return(False,errors)
          else:
              ret_user=userDB.objects.filter(email=postData['email'])
              if ret_user:
                  errors.append("Please use different login info!")
                  print "Please use different login info!"
                  return(False,errors)
              print "inside save"
              password=postData['password'].encode();
              hashed = bcrypt.hashpw(password, bcrypt.gensalt())
              newUser=userDB(first_name=postData['first_name'],last_name=postData['last_name'],email=postData['email'],password=hashed)
              newUser.save()
              print "after save"
              return(True,newUser)

# Create your models here.
class userDB(models.Model):
    # First Name - Required; No fewer than 2 characters; letters only
    # Last Name - Required; No fewer than 2 characters; letters only
    # Email - Required; Valid Format
    # Password - Required; No fewer than 8 characters in length; matches Password Confirmation
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    password = models.CharField(max_length=100)
    email=models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects=userDBManager()

class Author(models.Model):
     name = models.CharField(max_length=45)
     created_at = models.DateTimeField(auto_now_add = True)
     updated_at = models.DateTimeField(auto_now = True)

class booksDBManager(models.Manager):
    def createBook(self,postData):
         errors=[]
         if(postData['book_title']==""):
             errors.append('Please enter a title')
             return(False,errors)
         else:
             createdUser=userDB.objects.get(id=postData['id'])
             existingAuthor=Author.objects.get(id=postData['author'])
             if(existingAuthor):
                newAuthor=existingAuthor
             else:
                newAuthor=Author(name=postData['author_name'])
                newAuthor.save()
             newBook=Books(title=postData['book_title'],author=newAuthor)
             newBook.save()
             newReview=Reviews(review=postData['review'],rating=postData['rating'],book_rating=newBook,user_rating=createdUser)
             newReview.save()
             return(True,newBook)

class Books(models.Model):
    title = models.CharField(max_length=50)
    author = models.ForeignKey(Author)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return "title :"+self.title+"publishes date :"+str(self.published_date)
    def get_book_rating(self):
        revBook=Reviews.objects.filter(book_rating=self)
        return revBook
    objects=booksDBManager()

class reviewsDBManager(models.Manager):
    def createReview(self,postData):
        pass
    def updateReview(self,postData,id):
        errors=[]
        if(postData['review']=="") or (postData['rating']==""):
            errors.append('Please enter a review and rating')
            return(False,errors)
        else:
            reviewingUser=userDB.objects.get(id=postData['id'])
            reviewingBook=Books.objects.get(id=id)
            newReview=Reviews(review=postData['review'],rating=postData['rating'],book_rating=reviewingBook,user_rating=reviewingUser)
            newReview.save()
            return(True,newReview)

class Reviews(models.Model):
    review = models.CharField(max_length=50)
    rating = models.IntegerField()
    book_rating=models.ForeignKey(Books,related_name='rating_book')
    user_rating=models.ForeignKey(userDB,related_name='rating_user')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    def get_rating_list(self):
        listRate=[]
        for item in range(self.rating):
            listRate.append(item)
        return listRate
    def get_rating_list_white(self):
        listRate=[]
        for item in range(5-self.rating):
            listRate.append(item)
        return listRate

    objects=reviewsDBManager()
