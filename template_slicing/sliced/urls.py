from unicodedata import name
from django.urls import path
from . import views



urlpatterns = [
    path ('home', views.index , name="home"),
    path('login', views.login_view, name = 'login'),
    path('register', views.register, name = 'register'),
    path('logout', views.logout_view, name = 'logout'),
    path('adddiseases' , views.add_diseases, name='add_diseases'),
    path('list-diseases', views.listDisease, name = "listDisease"),
    path('editdisease/<int:ids>', views.edit_diseases, name="edit-disease"),
    path('deletedisease/<int:ids>', views.deletedisease, name="deletedisease"),
    path('addmedicine', views.add_medicine, name='add_medicine'),
    path('list-medicine', views.listmedicine, name = "listmedicine"),
    path('editmedicine/<int:ids>', views.edit_medicine, name="edit-medicine"),
    path('deletemedicine/<int:ids>', views.deletemedicine, name="deletemedicine"),
    path('addorders', views.add_orders, name="add_orders"),

]
