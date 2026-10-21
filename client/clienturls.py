"""
URL configuration for nexus13 project.

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
from client import clientviews

urlpatterns = [
    path('clientindex/', clientviews.index3),
    path('clientlogin/', clientviews.login),
    path('clientforget/', clientviews.forget),
    path('clientregister/', clientviews.register),
    path('clientsetpass/', clientviews.setpassword),
    path('clientprofile/', clientviews.clientprofile),
    path('clienteditprofile/<int:id>', clientviews.clienteditprofile),
    path('clientfamily/', clientviews.clientfamily),
    path('clientlogout/', clientviews.clientlogout),
                # genral function
    path('clientnotice/', clientviews.clientnotice),
    path('eventlist/', clientviews.eventlist),
    path('eventdetails/<int:id>', clientviews.eventdetails),
                # suggestion
    path('clientsuggestion/', clientviews.clientsuggestion),
    path('clientinsertsuggestion/', clientviews.clientinsertsuggestion),
    path('clientexpenceview/', clientviews.clientexpenceview),
                # visitor
    path('clientviewvisitor/', clientviews.clientviewvisitor),
    path('approve/<int:id>', clientviews.approve),
    path('refuce/<int:id>', clientviews.refuce),
    path('todayvisit/', clientviews.todayvisit),
                # clubhouse booking
    path('clubhousebooking/', clientviews.clubhousebooking),
    path('chstatus/', clientviews.chstatus),
    path('dd/', clientviews.dd), #ajax validation
    path('clubhousebooked/<int:id>',clientviews.clubhousebooked),
                # payment
    path('maintenance_payments/', clientviews.maintenance_payments),
    path('clientpayment/', clientviews.clientpayment),
    path('paysuccess/', clientviews.paysuccess),
    path('payfail/', clientviews.payfail),   
                # 
    path('notifications/', clientviews.view_notifications, name='view_notifications'),

]