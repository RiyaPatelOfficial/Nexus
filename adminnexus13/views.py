from django.shortcuts import render,redirect
from adminnexus13.models import *
from adminnexus13.forms import *
from django.contrib import messages
from datetime import datetime
from adminnexus13.function import handle_uploaded_file


def notify_unpaid_member(request, member_id):
    if request.method == 'POST':
        selected_month = request.session['selected_month']
        if selected_month:
            member = housing_member.objects.get(member_id=member_id)
            notification.objects.create(
                member_id=member,
                description=f"Reminder: Please pay your maintenance fee for {selected_month}.",
                notification_date=datetime.now(),
            )

            messages.success(request, f"Notification sent to {member.name}.")
        else:
            messages.error(request, "Please select a month to notify members.")

    return redirect('/maintenance-payment/') 

def maintenance_payment_view(request):
    selected_month = request.GET.get('month')
    request.session['selected_month']= "NUL"
    request.session['selected_month']=selected_month
    paid_members = []
    unpaid_members = []

    if selected_month:
        # Parse the selected month
        smonth = datetime.strptime(selected_month, '%Y-%m').month
        year = datetime.strptime(selected_month, '%Y-%m').year

        # print("----------month and year-----------",month,year)

        # Get all members
        all_members = housing_member.objects.all()

        # Get members who have paid for the selected month
        paid_members = maintenance_payment.objects.filter(
            # date_time__year=year,
            # date_time__month=month
            month=smonth
        ).values_list('member_id', flat=True)

        # Get members who haven't paid
        unpaid_members = all_members.exclude(member_id__in=paid_members)
    else:
        # If no month is selected, show all members who have paid
        paid_members = maintenance_payment.objects.all()

    context = {
        'paid_members': paid_members,
        'unpaid_members': unpaid_members,
        'selected_month': selected_month,
    }
    return render(request, 'maintenance_payment.html', context)

def reportexp(request):   
   
# def report_exp(request):
    selected_month = request.GET.get('month')
    expenses = []
    total_expense = 0

    if selected_month:
        # Extract the year and month from the selected_month value
        year, month = map(int, selected_month.split('-'))
        
        # Filter the expenses by the selected month
        expenses = expence.objects.filter(date_time__year=year, date_time__month=month)
        
        # Calculate the total expense
        total_expense = sum(exp.amount for exp in expenses)

    # Pass the filtered expenses and total to the template
    return render(request, 'reportexp.html', {
        'expenses': expenses,
        'selected_month': selected_month,
        'total_expense': total_expense
    })
   
        # this is the chbookcheck is report2 
def chbookcheck(request):
    bookings=clubhouse_booking.objects.all()
    if request.method== "POST":
        selected_date = request.POST.get("date")
        if selected_date:
            formatted_date = datetime.strptime(selected_date, "%Y-%m-%d").date()
            bookings = clubhouse_booking.objects.filter(start_date__date=formatted_date)

    context = {"e": bookings}
    return render(request, "report2.html", context)   

from django.shortcuts import render
from .models import housing_member, family_member

def filter_members(request):
    house_no = request.GET.get('house_no')
    block_no = request.GET.get('block_no')
    members = []
    total_members = 0

    if house_no and block_no:
        # Filter housing members based on house number and block
        members = housing_member.objects.filter(house_no=house_no, block_no=block_no)

        # Count total members including family members
        total_members = sum(
            1 + family_member.objects.filter(member_id=member.member_id).count()
            for member in members
        )

    return render(request, 'filter_members.html', {
        'members': members,
        'house_no': house_no,
        'block_no': block_no,
        'total_members': total_members
    })


def login(request):
    if request.method== "POST":
        uname=request.POST["email"]
        pwd=request.POST["password"]

        c=housing_member.objects.filter(email=uname,password=pwd,role="1").count()

        if c==1:

            obj=housing_member.objects.get(email=uname)
            request.session['adminname']=obj.name
            request.session['adminid']=obj.member_id
            request.session['email']=obj.email

            if request.POST.get("adminremember"):
                response = redirect("/")
                response.set_cookie('cookie_adminemail',request.POST['email'])
                response.set_cookie('cookie_adminpass',request.POST['password'])
                return response

            return redirect("/")
        else :
            messages.error(request,"Invalid username or password")
            return redirect("/")
        
    else:
        if request.COOKIES.get("cookie_email"):
            return render(request,"login.html",{'cookie_adminemail':request.COOKIES['cookie_adminemail'],'cookie_adminpass':request.COOKIES['cookie_adminpass']})
        else:
            return  render(request,"login.html" )

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

            return render(request,"resetpass.html")
    else:
        return render(request,"forget-password.html")
    
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
                return redirect("/login/")
            else:
                messages.error(request,"paas does not match")
                return render(request,"resetpass.html")
        else:
                messages.error(request,"invalid otp")
                return render(request,"resetpass.html")
        


def profile(request):
    c=housing_member.objects.filter(email= request.session['email']).count()
    
    if c ==1:
        obj=housing_member.objects.get(email=request.session['email'])
        return  render(request,"profile.html",{"e":obj})
    else:
        return redirect("/profile/") 
    
def editprofile(request,id):
    if request.method=="POST":
        e=housing_member.objects.get(member_id=id)
        f=housingform(request.POST,instance=e)
        print("---------------",f.errors)
        if f.is_valid():
            try:
                f.save()
                return redirect("/profile/")
            except:
                print("-------------------",sys.exc_info())
    else:
        e=housing_member.objects.get(member_id=id)
        return render(request,"editprofile.html",{"e":e}) 
    
def logout(request):
    try:
        del request.session['adminname']
        del request.session['adminid']
        del request.session['email']
        
        
        return redirect("/login/")   
    except:
        pass   

# =--------------------dashbord-----------------------d

def dashbord(request):

    if "adminid" in request.session:
        current_date=datetime.now().strftime("%Y-%m-%d")
        todayclub=clubhouse_booking.objects.filter(request_date=current_date)
        todaymain=maintenance_payment.objects.filter(date_time=current_date)
        return render(request,"dash-index.html",{"todayclub":todayclub,"todaymain":todaymain})    
    else:
        return redirect("/login/")  


# --------------11 table data---------------------

def table(request):
    if "adminid" in request.session:
        e=housing_member.objects.all()
        return  render(request,"users.html",{'e':e})   
    else:
        return redirect("/login/")

def family_table(request):
    if "adminid" in request.session:
        e=family_member.objects.all()
        return  render(request,"family_table.html",{'e':e})   
    else:
        return redirect("/login/")

def notifications(request):
    if "adminid" in request.session:
        e=notification.objects.all()
        return  render(request,"notification.html",{'e':e})   
    else:
        return redirect("/login/")

def noticeboards(request):
    if "adminid" in request.session:
        e=noticeboard.objects.all()
        return  render(request,"noticeboard.html",{'e':e})   
    else:
        return redirect("/login/")

def clubhouse_bookings(request):
    if "adminid" in request.session:
        e=clubhouse_booking.objects.all()
        return  render(request,"clubhouse_booking.html",{'e':e})   
    else:
        return redirect("/login/")

def maintenance_payments(request):
    if "adminid" in request.session:
        e=maintenance_payment.objects.all()
        return  render(request,"maintenance_payments.html",{'e':e})   
    else:
        return redirect("/login/")

def security_persons(request):
    if "adminid" in request.session:
        e=security_person.objects.all()
        return  render(request,"security_persons.html",{'e':e})   
    else:
        return redirect("/login/")

def visitorss(request):
    if "adminid" in request.session:
        e=visitors.objects.all()
        return  render(request,"visitorss.html",{'e':e})   
    else:
        return redirect("/login/")

def events(request):
    if "adminid" in request.session:
        e=event.objects.all()
        return  render(request,"events.html",{'e':e})   
    else:
        return redirect("/login/")

def event_gallerys(request):
    if "adminid" in request.session:
        e=event_gallery.objects.all()
        return  render(request,"event_gallerys.html",{'e':e})   
    else:
        return redirect("/login/")

def suggessions(request):
    if "adminid" in request.session:
        e=suggession.objects.all()
        return  render(request,"suggessions.html",{'e':e})   
    else:
        return redirect("/login/")

def expences(request):
    if "adminid" in request.session:
        e=expence.objects.all()
        return  render(request,"expences.html",{'e':e}) 
    else:
        return redirect("/login/")

def report(request):
    if "adminid" in request.session:
        e=maintenance_payment.objects.all()
        return  render(request,"report1.html",{'e':e}) 
    else:
            return redirect("/login/")

# -----------------------delete code---------------------------
def delexp(request,id):
    e=expence.objects.get(expence_id=id)
    e.delete()
    return redirect("/expence/")

def delsuggession(request,id):
    e=suggession.objects.get(suggession_id=id)
    e.delete()
    return redirect("/suggession/")

def delevent_gallery(request,id):
    e=event_gallery.objects.get(gallery_id=id)
    e.delete()
    return redirect("/event_gallery/")

def delevent(request,id):
    e=event.objects.get(event_id=id)
    e.delete()
    return redirect("/event/")

def delnoticeboard(request,id):
    e=noticeboard.objects.get(noticeboard_id=id)
    e.delete()
    return redirect("/noticeboard/")

# ----------------------insert code

import sys

def insertexpence(request):
    if request.method=="POST":
        f=expenceform(request.POST)
        print("---------------",f.errors)
        if f.is_valid():
            try:
                f.save()
                return redirect("/expence/")
            except:
                print("-------------------",sys.exc_info())
    else:
        return render(request,"expenceform.html")

def suggessionsform(request):
    e=housing_member.objects.all()
    if request.method=="POST":
        f=suggessionforms(request.POST)
        print("---------------",f.errors)
        if f.is_valid():
            try:
                f.save()
                return redirect("/suggession/")
            except:
                print("-------------------",sys.exc_info())
    else:
        return render(request,"suggessionsform.html",{'hsmember':e})

    
def insertevent_gallery(request):
    ev=event.objects.all()
    if request.method=="POST":
        f=insertevent_gallerys(request.POST,request.FILES)
        print("---------------",f.errors)
        if f.is_valid():
            try:
                handle_uploaded_file(request.FILES['img_path'])
                f.save()
                return redirect("/event_gallery/")
            except:
                print("-------------------",sys.exc_info())
    else:
        return render(request,"insertevent_gallery.html",{"ev":ev})

def insertevent(request):
    if request.method == "POST":
        form = insertevents(request.POST, request.FILES)  # Handle form and file uploads
        if form.is_valid():
            try:
                # Save the event
                event = form.save()

                # Step 1: Create notifications for all members
                members = housing_member.objects.all()  # Fetch all housing members
                for member in members:
                    notification.objects.create(
                        member_id=member,  # Link to each member
                        description=f"New Event: {event.event_name} has been added.",
                        notification_date=datetime.now()
                    )

                    # Step 2: Send Email
                    send_mail(
                        subject=f"New Event: {event.event_name}",
                        message=f"Dear {member.name},\n\nA new event has been scheduled:\n\n"
                                f"Event Name: {event.event_name}\n"
                                f"Description: {event.description}\n"
                                f"Start Date: {event.start_date}\n"
                                f"End Date: {event.end_date}\n\n"
                                "Thank you!",
                        from_email="gajjarbca@gmail.com",  # Replace with your email
                        recipient_list=[member.email],  # Send to the member’s email
                        fail_silently=True
                    )

                return redirect("/event/")

            except Exception as e:
                print(f"Error occurred: {e}")
                return render(request, "insertevent.html", {"error": "An error occurred. Please try again."})
        else:
            print("Form errors:", form.errors)
            return render(request, "insertevent.html", {"form": form})
    else:
        return render(request, "insertevent.html")
    
def insertvisitors(request):
    e=security_person.objects.all()
    if request.method=="POST":
        f=insertvisitorss(request.POST)
        print("---------------",f.errors)
        if f.is_valid():
            try:
                f.save()
                return redirect("/visitors/")
            except:
                print("-------------------",sys.exc_info())
    else:
        return render(request,"insertvisitors.html",{"e":e})
    
def insertnoticeboard(request):
    current_date = datetime.now().strftime("%Y-%m-%dT%H:%M") 

    if request.method == "POST":
        f = insertnoticeboards(request.POST)
        print("---------------", f.errors)
        if f.is_valid():
            try:
                # Save the new noticeboard
                new_notice = f.save()

                # Step 1: Notify all members
                members = housing_member.objects.all()
                for member in members:
                    notification.objects.create(
                        member_id=member,
                        description=f"New Notice: {new_notice.title} has been added.",
                        notification_date=datetime.now()
                    )

                    # Step 2: Send Email Notification
                    send_mail(
                        subject=f"New Notice: {new_notice.title}",
                        message=f"Dear {member.name},\n\nA new notice has been posted:\n\n"
                                f"Title: {new_notice.title}\n"
                                f"Description: {new_notice.description}\n"
                                f"Date: {new_notice.notice_date}\n\n"
                                "Thank you!",
                        from_email="gajjarbca@gmail.com",  # Replace with your actual email
                        recipient_list=[member.email],
                        fail_silently=True
                    )

                return redirect("/noticeboards/")
            except Exception as e:
                print(f"Error occurred: {e}")
    else:
        return render(request, "insertnoticeboard.html", {"current_date": current_date})

def insertsecurity(request):
    if request.method=="POST":
        f=insertsecuritys(request.POST)
        print("---------------",f.errors)
        if f.is_valid():
            try:
                f.save()
                return redirect("/security_person/")
            except:
                print("-------------------",sys.exc_info())
    else:
        return render(request,"insertsecurity.html")

        # ----------------------------------------------
                # update
        # ----------------------------------------------

def updateexpence(request,id):
    if request.method=="POST":
        e=expence.objects.get(expence_id=id)
        f=expenceform(request.POST,instance=e)
        print("---------------",f.errors)
        if f.is_valid():
            try:
                f.save()
                return redirect("/expence/")
            except:
                print("-------------------",sys.exc_info())
    else:
        e=expence.objects.get(expence_id=id)
        return render(request,"updateexpence.html",{'eexpence':e})

def updatesuggessions(request,id):
    hs=housing_member.objects.all()
    if request.method=="POST":
        e=suggession.objects.get(suggetion_id=id)
        f=suggessionforms(request.POST,instance=e)
        print("---------------",f.errors)
        if f.is_valid():
            try:
                f.save()
                return redirect("/suggession/")
            except:
                print("-------------------",sys.exc_info())
    else:
        s=suggession.objects.get(suggetion_id=id)
        return render(request,"updatesuggessions.html",{'suggetion':s,"hsmember":hs})


    
def updateevent_gallery(request,id):
    ev=event.objects.all()
    if request.method=="POST":
        e=event_gallery.objects.get(gallery_id=id)
        f=insertevent_gallerys(request.POST,instance=e)
        print("---------------",f.errors)
        if f.is_valid():
            try:
                f.save()
                return redirect("/event/")
            except:
                print("-------------------",sys.exc_info())
    else:
        e=event_gallery.objects.get(gallery_id=id)
        return render(request,"updateevent_gallery.html",{"e":e,"ev":ev})
    
def updateevent(request, id):
    if request.method == "POST":
        e = event.objects.get(event_id=id)
        f = insertevents(request.POST, instance=e)
        print("---------------", f.errors)
        if f.is_valid():
            try:
                # Save the updated event
                updated_event = f.save()

                # Step 1: Notify all members
                members = housing_member.objects.all()
                for member in members:
                    notification.objects.create(
                        member_id=member,  # Link notification to the member
                        description=f"Event Updated: {updated_event.event_name} has been updated.",
                        notification_date=datetime.now()
                    )

                    # Step 2: Send Email Notification
                    send_mail(
                        subject=f"Event Updated: {updated_event.event_name}",
                        message=f"Dear {member.name},\n\nThe event has been updated:\n\n"
                                f"Event Name: {updated_event.event_name}\n"
                                f"Description: {updated_event.description}\n"
                                f"Start Date: {updated_event.start_date}\n"
                                f"End Date: {updated_event.end_date}\n\n"
                                "Thank you!",
                        from_email="gajjarbca@gmail.com",  # Replace with your actual email
                        recipient_list=[member.email],  # Send to the member’s email
                        fail_silently=True
                    )

                return redirect("/event/")

            except Exception as e:
                print(f"Error occurred: {e}")
                return render(request, "updateevent.html", {"e": e, "error": "An error occurred. Please try again."})
        else:
            return render(request, "updateevent.html", {"e": e, "form_errors": f.errors})

    else:
        e = event.objects.get(event_id=id)
        return render(request, "updateevent.html", {"e": e})

    
def updatevisitors(request,id):
    s=security_person.objects.all()
    if request.method=="POST":
        e=visitors.objects.get(visitor_id=id)
        f=insertvisitorss(request.POST,instance=e)
        print("---------------",f.errors)
        if f.is_valid():
            try:
                f.save()
                return redirect("/visitors/")
            except:
                print("-------------------",sys.exc_info())
    else:
        e=visitors.objects.get(visitor_id=id)
        return render(request,"updatevisitors.html",{"e":e,"s":s})
    
def updatenoticeboard(request, id):
    notice = noticeboard.objects.get(noticeboard_id=id)  # Fixing incorrect field name

    if request.method == "POST":
        f = insertnoticeboards(request.POST, instance=notice)  # Correcting form usage
        print("---------------", f.errors)
        if f.is_valid():
            try:
                # Save the updated noticeboard
                updated_notice = f.save()

                # Step 1: Notify all members
                members = housing_member.objects.all()
                for member in members:
                    notification.objects.create(
                        member_id=member,
                        description=f"Notice Updated: {updated_notice.title} has been updated.",
                        notification_date=datetime.now()
                    )

                    # Step 2: Send Email Notification
                    send_mail(
                        subject=f"Notice Updated: {updated_notice.title}",
                        message=f"Dear {member.name},\n\nA notice has been updated:\n\n"
                                f"Title: {updated_notice.title}\n"
                                f"Description: {updated_notice.description}\n"
                                f"Date: {updated_notice.notice_date}\n\n"
                                "Thank you!",
                        from_email="gajjarbca@gmail.com",  # Replace with your actual email
                        recipient_list=[member.email],
                        fail_silently=True
                    )

                return redirect("/noticeboards/")
            except Exception as e:
                print(f"Error occurred: {e}")
    else:
        return render(request, "updatenoticeboard.html", {"notice": notice})

def updatesecurity(request,id):
    if request.method=="POST":
        e=security_person.objects.get(security_id=id)
        f=insertsecuritys(request.POST,instance=e)
        print("---------------",f.errors)
        if f.is_valid():
            try:
                f.save()
                return redirect("/security_person/")
            except:
                print("-------------------",sys.exc_info())
    else:
        e=security_person.objects.get(security_id=id)
        return render(request,"updatesecurity.html",{"e":e})
    
def chapprove(request,id):
    obj = clubhouse_booking.objects.filter(clubhouse_booking_id=id).count()

    if obj == 1:
        v_status = clubhouse_booking.objects.get(clubhouse_booking_id=id)
        v_status.booking_status=1
       
        v_status.save()
        return redirect("/clubhouse_bookings/")
    else:
        return redirect("/clubhouse_bookings/")

def chrefuce(request,id):
    obj = clubhouse_booking.objects.filter(clubhouse_booking_id=id).count()

    if obj == 1:
        v_status = clubhouse_booking.objects.get(clubhouse_booking_id=id)
        v_status.booking_status=2
        v_status.save()
        return redirect("/clubhouse_bookings/")
    else:
        return redirect("/clubhouse_bookings/")