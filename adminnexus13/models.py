from django.db import models

#1.FOR HOUSING MEMBER
class housing_member(models.Model):
    member_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=50)
    house_no=models.CharField(max_length=5)
    block_no=models.CharField(max_length=3)
    contact=models.CharField(max_length=10)
    email=models.CharField(max_length=150,unique=True)
    password=models.CharField(max_length=10)
    role= models.IntegerField(null=True)
    otp=models.CharField(max_length=10)
    otp_used=models.IntegerField(null=True)
    
    class Meta:  
        db_table="housing_member"
        
#2.FOR FAMILY MEMBER
class family_member(models.Model):
    family_id=models.AutoField(primary_key=True)
    member_id = models.ForeignKey(housing_member,null=True,on_delete=models.SET_NULL)
    member_name=models.CharField(max_length=50)
    relationship=models.CharField(max_length=30)
    contact=models.CharField(max_length=10)
    
    class Meta:
        db_table="family_member"

#3.FOR NOTIFICATION
class notification(models.Model):
    notification_id=models.AutoField(primary_key=True)
    member_id = models.ForeignKey(housing_member,null=True,on_delete=models.SET_NULL)
    description=models.CharField(max_length=500)
    notification_date=models.DateTimeField()
   
    class Meta:
        db_table="notification"
        
#4.FOR NOTICEBOARD delete instert
class noticeboard(models.Model):
    noticeboard_id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=250)
    description=models.CharField(max_length=250)
    notice_date=models.DateTimeField()
        
    class Meta:
        db_table="noticeboard"

        
#5.FOR CLUBHOUSE BOOKING 
class clubhouse_booking(models.Model):
    clubhouse_booking_id=models.AutoField(primary_key=True)
    member_id= models.ForeignKey(housing_member,null=True,on_delete=models.SET_NULL)
    start_date=models.DateTimeField()
    end_date = models.DateTimeField()
    request_date=models.DateTimeField()
    description=models.CharField(max_length=250)
    booking_status=models.CharField(max_length=1)
    payment_status = models.CharField(max_length=1)
    amount=models.IntegerField()
    
    class Meta:
        db_table="clubhouse_booking"
        
# 6.FOR MAINTENANCE PAYMENT
class maintenance_payment(models.Model):
    payment_id=models.AutoField(primary_key=True)
    member_id = models.ForeignKey(housing_member,null=True,on_delete=models.SET_NULL)
    date_time=models.DateTimeField()
    amount= models.IntegerField()
    month = models.IntegerField()
    description=models.CharField(max_length=250)
    payment_status = models.CharField(max_length=1)
    class Meta:
        db_table="maintenance_payment"

#7.FOR SECURITY PERSON  insert
class security_person(models.Model):
    security_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=250)
    email=models.CharField(max_length=150,unique=True)
    password =models.CharField(max_length=10)
    contact=models.CharField(max_length=10)
    id_proof = models.CharField(max_length=150)

    class Meta:
        db_table="security_person"


#8.FOR VISITORS insert 
class visitors(models.Model):
    visitor_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=100)
    contact_no=models.CharField(max_length=10)
    house_no=models.CharField(max_length=5)
    block_no =models.CharField(max_length=3)
    description=models.CharField(max_length=250)
    date_time=models.DateTimeField()
    registered_by = models.ForeignKey(security_person,null=True,on_delete=models.SET_NULL)
    status= models.IntegerField()

    class Meta:
        db_table="visitors"


#9.FOR EVENT  delete insert
class event(models.Model):
    event_id=models.AutoField(primary_key=True)
    event_name=models.CharField(max_length=100)
    description=models.CharField(max_length=250)
    start_date=models.DateTimeField()
    end_date=models.DateTimeField()
    epost=models.CharField(max_length=150)
    
    class Meta:
        db_table="event"
          
#10.FOR EVENT GALLERY delete insert
class event_gallery(models.Model):
    gallery_id=models.AutoField(primary_key=True)
    event_id = models.ForeignKey(event,null=True,on_delete=models.SET_NULL)
    img_path=models.CharField(max_length=150)
    uploaded_by = models.ForeignKey(housing_member,null=True,on_delete=models.SET_NULL)
    
    class Meta:
        db_table="event_gallery"

        
#11.FOR SUGGETION delete insert
class suggession(models.Model):
    suggetion_id=models.AutoField(primary_key=True)
    description=models.CharField(max_length=250)
    suggested_by=models.ForeignKey(housing_member,null=True,on_delete=models.SET_NULL)
    
    class Meta:
        db_table="suggession"

#expence table  delete insert
class expence(models.Model):
    expence_id=models.AutoField(primary_key=True)
    description=models.CharField(max_length=250)
    amount= models.IntegerField()
    date_time=models.DateTimeField()
    expence_type=models.CharField(max_length=250)
    paid_to=models.CharField(max_length=250)
    
    class Meta:
        db_table="expence"