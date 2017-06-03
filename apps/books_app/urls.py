from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.index,name='index'),
    url(r'^login$',views.login,name='login'),
    url(r'^register$',views.register,name='register'),
    url(r'^reg_home$',views.reg_home,name='reghome'),
    url(r'^logout$',views.logout,name='logout'),
    url(r'^newauthor$',views.newauthor,name='newauthor'),
    url(r'^newbook/(?P<id>\d+)$',views.newbook,name='newbook'),
    url(r'^add$',views.add,name='add'),
    url(r'^books$',views.books,name='books'),
    url(r'^review/(?P<id>\d+)$',views.review,name='review'),
    url(r'^users/(?P<id>\d+)$',views.users,name='users'),
    url(r'^showAdd$',views.showAdd,name='showAdd'),
    url(r'^update/(?P<id>\d+)$',views.update,name='update')
]
