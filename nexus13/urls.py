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
from django.urls import path,include
from adminnexus13 import views
from client import clienturls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login),
    path('logout/', views.logout),
    path('', views.dashbord),
    path('forget/', views.forget),
    path('reset/', views.setpassword),
    path('profile/', views.profile),
    path('editprofile/<int:id>', views.editprofile),
    path('table/', views.table),
    path('family/', views.family_table),
    path('notifications/', views.notifications),
    path('noticeboards/', views.noticeboards),
    path('clubhouse_bookings/', views.clubhouse_bookings),
    path('maintenance_payment/', views.maintenance_payments),
    path('security_person/', views.security_persons),
    path('visitors/', views.visitorss),
    path('event/', views.events),
    path('event_gallery/', views.event_gallerys),
    path('suggession/', views.suggessions),
    path('expence/', views.expences),
    path('report/', views.report),
    # delete urls
    path('delexp/<int:id>',views.delexp),
    path('delsuggession/<int:id>',views.delsuggession),
    path('delevent_gallery/<int:id>',views.delevent_gallery),
    path('delevent/<int:id>',views.delevent),
    path('delnoticeboard/<int:id>',views.delnoticeboard),    
                 # insert urls
    path('insertexpence/', views.insertexpence),
    path('insertsuggession/', views.suggessionsform),
    path('insertevent_gallery/', views.insertevent_gallery),
    path('insertevent/', views.insertevent),
    path('insertvisitors/', views.insertvisitors),
    path('insertnoticeboard/', views.insertnoticeboard),
    path('insertsecurity/', views.insertsecurity),
                 # update urls
    path('updateexpence/<int:id>', views.updateexpence),
    path('updatesuggession/<int:id>', views.updatesuggessions),
    path('updateevent_gallery/<int:id>', views.updateevent_gallery),
    path('updateevent/<int:id>', views.updateevent),
    path('updatevisitors/<int:id>', views.updatevisitors),
    path('updatenoticeboard/<int:id>', views.updatenoticeboard),
    path('updatesecurity/<int:id>', views.updatesecurity),
        #clubhouse 
    path('chapprove/<int:id>',views.chapprove),
    path('chrefuce/<int:id>',views.chrefuce),
        # maitenance payment
    path('maintenance-payment/', views.maintenance_payment_view, name='maintenance_payments'), #with filters of maitenance
    path('maintenance/notify/<int:member_id>/', views.notify_unpaid_member, name='notify_member'),
    # path('maintenance/notify_all/', views.notify_all_unpaid_members, name='notify_all'),
        # report
    path("reportexp/",views.reportexp),
    path('filtermembers/', views.filter_members, name='filter_members'),
    path("chbookcheck/",views.chbookcheck),
        
        # APPLICATION
    path('client/',include('client.clienturls')),
    path('sp/',include('securityperson.spurls')),

]