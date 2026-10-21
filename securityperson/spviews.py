from django.shortcuts import render,redirect
from adminnexus13.models import *
from adminnexus13.forms import *

# Create your views here.
def spviewvisitor(request):
    e=visitors.objects.all()
    return  render(request,"spviewvisitor.html",{'e':e})  

import sys
from datetime import datetime
from nexus13 import settings
from django.core.mail import send_mail

def spinsertvisitor(request):
    e=security_person.objects.all()
    secid=request.session['id']
    c=current_date=datetime.now().strftime("%Y-%m-%dT%H:%M") # for register date 
    if request.method=="POST":
        f=insertvisitorss(request.POST)
        print("---------------",f.errors)
        if f.is_valid():
            try:
                # line after try hno,bno use to fetch ans send data to client side
                bno = request.POST["block_no"]
                hno = request.POST["house_no"]  
                urrent_date = datetime.now() #send current date into notification table print("-----------------------member-------")
                obj = housing_member.objects.get(house_no=hno,block_no=bno)
                print("----------Fetch done--------",obj)
                e= obj.email
                subject = 'new visitor arrivied'
                messages = str("hi there are few visitor are waiting ")
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [e, ]

                send_mail(subject,messages,email_from,recipient_list)

                n = notification(member_id_id=obj.member_id,description="hi a new visitor arrivied at your house you want allow !!",notification_date=current_date)
                n.save()
                # n = notification used to store data in notification table n.save save data in table
                f.save()
                return redirect("/sp/spviewvisitor/")
            except:
                print("-------===+++===--------",sys.exc_info())
    else:
        return render(request,"spinsertvisitor.html",{"e":e,"c":c,"secid":secid}) # above register date pass 


from adminnexus13.models import *
from adminnexus13.forms import *
from django.contrib import messages


def splogin(request):
    if request.method== "POST":
        uname=request.POST["email"]
        pwd=request.POST["password"]

        c=security_person.objects.filter(email=uname,password=pwd).count()

        if c==1:

            obj=security_person.objects.get(email=uname)
            request.session['seqname']=obj.name
            request.session['seqid']=obj.security_id
            request.session['email']=obj.email

            if request.POST.get("remember"):
                response = redirect("/sp/spviewvisitor/")
                response.set_cookie('cookie_email',request.POST['email'])
                response.set_cookie('cookie_pass',request.POST['password'])
                return response

            return redirect("/sp/spviewvisitor/")
        else :
            messages.error(request,"Invalid username or password contact admin if you forget")
            return redirect("/sp/splogin/")
        
    else:
        if request.COOKIES.get("cookie_email"):
            return render(request,"splogin.html",{'cookie_email':request.COOKIES['cookie_email'],'cookie_pass':request.COOKIES['cookie_pass']})
        else:
            return  render(request,"splogin.html")
        
def splogout(request):
    try:
        del request.session['seqname']
        del request.session['seqid']
        del request.session['email']
        
        
        return redirect("/login/")   
    except:
        pass 

import random
from nexus13 import settings
from django.core.mail import send_mail
    
def spprofile(request):
    c=security_person.objects.filter(email= request.session['email']).count()
    
    if c ==1:
        obj=security_person.objects.get(email=request.session['email'])
        return  render(request,"spprofile.html",{"e":obj})
    else:
        return redirect("/sp/splogin/") 
    
def speditprofile(request,id):
    if request.method=="POST":
        e=security_person.objects.get(member_id=id)
        f=security_person(request.POST,instance=e)
        print("---------------",f.errors)
        if f.is_valid():
            try:
                f.save()
                return redirect("/sp/spprofile/")
            except:
                print("-------------------",sys.exc_info())
    else:
        e=security_person.objects.get(member_id=id)
        return render(request,"speditprofile.html",{"e":e})  
