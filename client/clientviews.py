from django.shortcuts import render,redirect
from adminnexus13.models import *
from adminnexus13.forms import *
from django.contrib import messages
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
# from django.contrib.auth.decorators import login_required

# # @login_required
def view_notifications(request):
    # Assuming you have a `user` linked to `housing_member`
    member = request.session["id"]
    notifications = notification.objects.filter(member_id=member).order_by('-notification_date')
    
    return render(request, "notifications.html", {"notifications": notifications})

    # clubhouse code
    # clubhouse while payment after apprrove
    
@csrf_exempt
def clubhousebooked(request,id):  
    if request.method=="POST":
        e=clubhouse_booking.objects.get(clubhouse_booking_id=id)
        
        stformatted_datetime = e.start_date.strftime("%Y-%m-%d %H:%M:%S")
        e.start_date=stformatted_datetime
        endstformatted_datetime=e.end_date.strftime("%Y-%m-%d %H:%M:%S")
        e.start_date=endstformatted_datetime
        reqdate=e.end_date.strftime("%Y-%m-%d %H:%M:%S")
        e.request_date=reqdate
        e.description=request.POST["description"]
        e.amount=request.POST["amount"]
        e.payment_status="1"
        e.booking_status="1"

        e.save()
        return redirect("/client/chstatus/")   
    else:
        e=expence.objects.get(expence_id=id)
        return render(request,"clubhousebookstatus.html",{'e':e})  

    

# insert clubhousebooking code

def clubhousebooking(request):
    if 'id' in request.session:
        current_date=datetime.now().strftime("%Y-%m-%d %H:%M") 
        name=request.session['id']

        if request.method=="POST":
            chmember =request.POST["member_id"]
            ch_start_date = request.POST["start_date"]
            ch_end_date = request.POST["end_date"]
            ch_request_date = request.POST["request_date"]
            chpayment_status = request.POST["payment_status"]
            chbooking_status =request.POST["booking_status"]
            chdescription =request.POST["description"]
            chamounts = request.POST["amount"]
            
            clubhouse_book =clubhouse_booking(
                member_id_id=chmember,
                start_date=ch_start_date,
                end_date=ch_end_date,
                description=chdescription,
                request_date=ch_request_date,
                payment_status=chpayment_status,
                booking_status=chbooking_status,
                amount=chamounts)

            if chamounts > "0":
                clubhouse_book.save()
                return redirect('/client/chstatus')         
            else:   
                messages.error(request,"select proper date")
                return redirect("/client/clubhousebooking/")
        else:
            return  render(request,"clubhousebooking.html",{"uname":name,"current_date":current_date })
    else :
        return redirect('/client/clientlogin')
    
#   just ajax validation for date selection

def dd(request):   
    if request.method=="POST":
        start_date= request.POST.get("start_date")
        end_date= request.POST.get("end_date")
        
        st = datetime.strptime(start_date, "%Y-%m-%d")
        et = datetime.strptime(end_date, "%Y-%m-%d")
        
        day_difference= (et-st).days 
        if day_difference == 0:
            day_difference=1
        
        amount=day_difference * 500
        if amount < 0:
            messages.error(request,"invalid date  select proper date ")
        print("=++++++++++++++++++++++=",day_difference)
        print("------------amount-----------",amount)

        return JsonResponse({"amount": amount})
    else:
        return render(request,"datediff.html")

def chstatus(request):
    if 'id' in request.session:
        a=request.session['id']
        e=clubhouse_booking.objects.filter(member_id=a)
        print("--status csfs--time---",e)
        return  render(request,"clubhousebookstatus.html",{'e':e})
    else :
        return redirect('/client/clientlogin')
    

# clubhouse all code end
    

#maintenace payment code

def maintenance_payments(request):
    if 'id' in request.session:
        a=request.session['id']
        e=maintenance_payment.objects.filter(member_id=a)
        print("--maintenance--time---",e)
        return  render(request,"clientmaintenance.html",{'e':e})
    else :
        return redirect('/client/clientlogin')

def clientpayment(request):
    member_id = request.session.get('id')  # Assuming member ID is stored in the session
    current_date=datetime.now().strftime("%Y-%m-%d %H:%M") 
    
    # Get all months already paid for the current year
    paid_months = (
        maintenance_payment.objects.filter(member_id=member_id, payment_status='1')
        .values_list('month', flat=True)
    )
    
    return render(request, 'clientpayment.html', {
        'paid_months': list(paid_months),
        'current_date': current_date,
    })

@csrf_exempt
def paysuccess(request):
    member_id = request.POST.get('member_id')
    month = request.POST.get('month')

    # Check if the payment already exists for the given month
    if maintenance_payment.objects.filter(member_id=member_id, month=month, payment_status='1').exists():
        return JsonResponse({"error": "Payment for this month has already been made."}, status=400)
   
    if request.method=="POST":
        f=maintenanaceform(request.POST)
        print("------------------f----",f)
        print("---------------",f.errors)
        if f.is_valid():
            try:
                f.save()
                return redirect("/client/paysuccess/")
            except:
                print("-------------------",sys.exc_info())
    else:
        return  render(request,"paymentsuccess.html")

def payfail(request):
    return  render(request,"paymentfail.html")

    #index and other page start
def index3(request):

    if 'id' in request.session:
        current_date=datetime.now().strftime("%Y-%m-%d")
        current_datech=datetime.now().strftime("%Y-%m-%d %H:%M") 

        name=request.session['id']
        new_notice=noticeboard.objects.filter(notice_date__date=current_date)

        new_event=event.objects.filter(start_date__date=current_date)
        return  render(request,"index-3.html",{"new_notice":new_notice,"new_event":new_event,"current_date":current_datech})
    else:
        return redirect('/client/clientlogin')


        # login,forget,set password,register,logout
def login(request):
    if request.method== "POST":
        uname=request.POST["email"]
        pwd=request.POST["password"]

        c=housing_member.objects.filter(email=uname,password=pwd).count()

        if c==1:

            obj=housing_member.objects.get(email=uname)
            request.session['name']=obj.name
            request.session['id']=obj.member_id
            request.session['email']=obj.email
            request.session['house_no']=obj.house_no
            request.session['block_no']=obj.block_no

            print("------------------------",request.session['name'])
            print("------------------------",request.session['id'])
            print("------------------------",request.session['email'])
           

            if request.POST.get("cremember"):
                response = redirect("/client/clientprofile/")
                response.set_cookie('cookie_email',request.POST['email'])
                response.set_cookie('cookie_pass',request.POST['password'])
                return response

            return redirect("/client/clientprofile/")
        else :
            messages.error(request,"Invalid username or password")
            return redirect("/client/clientlogin/")
        
    else:
        if request.COOKIES.get("cookie_email"):
            return  render(request,"clientlogin.html",{'cookie_email':request.COOKIES['cookie_email'],'cookie_pass':request.COOKIES['cookie_pass']})
        else:
            return  render(request,"clientlogin.html")


import random
from nexus13 import settings
from django.core.mail import send_mail
    
def forget(request):
    if request.method == "POST":
        e=request.POST["email"]
        otp1 = random.randint(1000,9999)
        obj = housing_member.objects.filter(email=e).count()

        if obj == 1:
         
            val=housing_member.objects.filter(email=e).update(otp= otp1,otp_used=0)
          
            request.session["temail"]=e
            
            print("------================-------",request.session["temail"])

            subject = 'otp verification from housing maintenance service'
            messages = str(otp1)
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [e, ]

            send_mail(subject,messages,email_from,recipient_list)

            return render(request,"clientsetpass.html")
    else:
        return render(request,"clientforget.html")

def setpassword(request):
    if request.method == "POST":
        uotp = request.POST['otp']
        p = request.POST['password']
        cpass = request.POST['cpassword']   
       
        e = request.session["temail"]

        print("============================",request.session["temail"])

        val = housing_member.objects.filter(email=e,otp=uotp,otp_used=0).count()

        if val == 1:
            if p== cpass:
                e =housing_member.objects.filter(email=e).update(password= p,otp_used=1)
                return redirect("/client/clientlogin/")
            else:
                messages.error(request,"paas does not match")
                return render(request,"clientsetpass.html")
        else:
                messages.error(request,"invalid otp")
                return render(request,"resetpass.html")


import sys

def register(request):
    if request.method=="POST":
        f=housingform(request.POST)
        print("---------------",f.errors)
        if f.is_valid():
            try:
                f.save()
                return redirect("/client/clientlogin/")
            except:
                print("-------------------",sys.exc_info())
    else:
        return  render(request,"clientregister.html")
    

def clientlogout(request):
    try:
        del request.session['name']
        del request.session['id']
        del request.session['email']
        del request.session['house_no']
        del request.session['block_no']
        
        return redirect("/client/clientlogin/")   
    except:
        pass

        # profile and edit profile

def clientprofile(request):
    if 'id' in request.session:
        c = housing_member.objects.filter(email= request.session['email']).count() 
        if c == 1:
            obj = housing_member.objects.get(email=request.session['email'])
            return  render(request,"clientprofile.html",{"e":obj})
        else:
            return  redirect("/client/clientprofile/")
    else :
        return redirect('/client/clientlogin')
              
def clienteditprofile(request,id):
    if 'id' in request.session:
        if request.method=="POST":
            request.session['name']=request.POST["name"]
            e=housing_member.objects.get(member_id=id)
            f=housingform(request.POST,instance=e)
            print("---------------",f.errors)
            if f.is_valid():
                try:
                    f.save()
                    return redirect("/client/clientprofile/")
                except:
                    print("-------------------",sys.exc_info())
        else:
            e=housing_member.objects.get(member_id=id)
            return render(request,"updateprofile.html",{"e":e})
    else :
        return redirect('/client/clientlogin')
    
    # insert family details

def clientfamily(request):
    name=request.session['id']
    e=family_member.objects.filter(member_id=request.session['id'])
    if request.method=="POST":
        f=familyform(request.POST)
        print("---------------",f.errors)
        if f.is_valid():
            try:
                f.save()
                return redirect("/client/clientprofile/")
            except:
                print("-------------------",sys.exc_info())
    else:
        return  render(request,"insertfamily.html",{"uname":name,"e":e})
      
# watch noticeboard

def clientnotice(request):
    e=noticeboard.objects.all().order_by('-notice_date')
    return  render(request,"clientnotice.html",{"e":e})

# eventlist and details(gallery) 

def eventlist(request):
    if 'id' in request.session:
        e=event.objects.all()
        return render(request,"eventlist.html",{"e":e})
    else :
        return redirect('/client/clientlogin')

def eventdetails(request,id):
    c1=event_gallery.objects.filter(event_id=id)
    ev_desc=event.objects.filter(event_id=id)
    e=event_gallery.objects.filter(event_id=id).count()
    print("------------count--------",e,ev_desc)
    if e >= 0:
        c=event_gallery.objects.filter(event_id=id)
        print("-------c----------",c,)
        return render(request,"eventdetails.html",{"c":c ,"ev_desc":ev_desc})
    else:
        print("-------c1---------------",c1)
        return render(request,"eventdetails.html",{"c":c1})
    
    # show suggestion insert suggestion
      
def clientsuggestion(request):
    if 'id' in request.session:
        e=suggession.objects.all()
        return  render(request,"clientsuggestion.html",{"e":e})
    else :
        return redirect('/client/clientlogin')  
    

def clientinsertsuggestion(request):
    name=request.session['id']
    e=housing_member.objects.all()
    if request.method=="POST":
        f=suggessionforms(request.POST)
        print("---------------",f.errors)
        if f.is_valid():
            try:
                f.save()
                return redirect("/client/clientsuggestion/")
            except:
                print("-------------------",sys.exc_info())
    else:
        return render(request,"insertsuggestion.html",{'hsmember':e,"uname":name})
      
 # show expernce of society

def clientexpenceview(request):
    if 'id' in request.session:
        e=expence.objects.all()
        return  render(request,"clientexpenceview.html",{'e':e}) 
    else :
        return redirect('/client/clientlogin')
      
# visitor code start with security person 

def clientviewvisitor(request):
    if "house_no" in request.session:
        a=request.session['house_no']
        b=request.session['block_no']
        e=visitors.objects.filter(house_no=a,block_no=b)
        print("-visitors---time---",e)
        return  render(request,"clientviewvisitor.html",{'e':e})
    else:
        return redirect('/client/clientlogin')

# visitors approve
def approve(request,id):    
    obj = visitors.objects.filter(visitor_id=id).count()

    if obj == 1:
        v_status = visitors.objects.get(visitor_id=id)
        v_status.status=1
        v_status.save()
        return redirect("/client/clientviewvisitor/")
    else:
        return redirect("/client/clientviewvisitor/")
# visitors refuce
def refuce(request,id):
    obj = visitors.objects.filter(visitor_id=id).count()

    if obj == 1:
        v_status = visitors.objects.get(visitor_id=id)
        v_status.status=2
        v_status.save()
        return redirect("/client/clientviewvisitor/")
    else:
        return redirect("/client/clientviewvisitor/")

def todayvisit(request):
    h_m = housing_member.objects.get(email=request.session['email'])
    b_no= h_m.block_no
    h_no= h_m.house_no
    date= datetime.now().strftime("%Y-%m-%d")
    print("---date ---",date)
    c= visitors.objects.filter(house_no=h_no,block_no=b_no,date_time__date=date)
    print("--------cc ---",c)
    return render(request,"clientviewvisitor.html",{'e':c})
    
