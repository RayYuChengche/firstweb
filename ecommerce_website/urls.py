"""
URL configuration for ecommerce_website project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from store.views import product_list , about , add_to_cart , view_cart , checkout , order_success , reservation_success  , make_reservation
from store import views




urlpatterns = [
    path("admin/", admin.site.urls),
    path("", about, name="about"),
    path("about/", about, name="about"),
    path('add_to_cart/<int:product_id>/' , add_to_cart, name='add_to_cart'),
    path('view_cart/' , view_cart, name='view_cart'),
    path('checkout/' , checkout, name='checkout'),
    path('order_success/', order_success, name='order_success'),   
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('student/', views.student_home, name='student_home'),
    path('teacher/', views.teacher_home, name='teacher_home'), 
    path("product_list/", product_list, name="product_list"),
    path('success/', views.reservation_success, name='reservation_success'),
    path('reservation_success/<int:email_sent>/', reservation_success, name='reservation_success'),
    path("make_reservation/", make_reservation, name="make_reservation"),
    path("success1/", views.success1, name="success1"),
    path("success2/", views.success2, name="success2"),

]

