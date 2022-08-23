from django.urls import path
from . import views



urlpatterns = [
    path('', views.index, name = 'index'),
    path('userLogin', views.login_view, name='userLogin'),
    path('userRegister', views.register, name='userRegister'),
    path('userLogout', views.logout_view, name='userLogout'),
    path('getMedicine/<int:disId>', views.getMedicine, name = 'getMedicine'),
    path('viewMedDetail/<int:medId>', views.viewMedDetail, name = 'viewMedDetail'),
    path('addToCart/<int:medId>', views.addToCart, name = 'addToCart'),
    path('viewCart', views.viewCart, name = 'viewCart'),
    path('removeItemCart/<int:id>', views.removeItemCart, name='removeItemCart'),
    path('checkOut', views.checkOut, name='checkOut'),
    path('allOrders', views.allOrders, name='allOrders')
]