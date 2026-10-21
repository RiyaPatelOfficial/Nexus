from django import forms
from adminnexus13.models import *

class expenceform(forms.ModelForm):
    class Meta:
        model=expence
        fields=["description","amount","date_time","expence_type","paid_to"]

class suggessionforms(forms.ModelForm):
    class Meta:
        model=suggession 
        fields=["description","suggested_by"]

class insertevent_gallerys(forms.ModelForm):
    img_path = forms.FileField()  # for creating file input
    class Meta:
        model=event_gallery
        fields=["event_id","img_path"]

class insertevents(forms.ModelForm):
    class Meta:
        model=event
        fields=["event_name","description","epost","start_date","end_date"]

class insertvisitorss(forms.ModelForm):
    class Meta:
        model=visitors
        fields=["name","contact_no","house_no","block_no","description","date_time","status","registered_by"]

class insertnoticeboards(forms.ModelForm):
    class Meta:
        model=noticeboard
        fields=["title","description","notice_date"]

class insertsecuritys(forms.ModelForm):
    class Meta:
        model=security_person
        fields=["name","email","contact","id_proof","password"]

        #client side

class housingform(forms.ModelForm):
    class Meta:
        model=housing_member
        fields=["name","house_no","block_no","contact","email","password"]

class familyform(forms.ModelForm):
    class Meta:
        model=family_member
        fields=["member_id","member_name","relationship","contact"]

class clubhouseform(forms.ModelForm):
    class Meta:
        model=clubhouse_booking 
        fields=["member_id","start_date","end_date","request_date","description","amount","payment_status","booking_status"]
    

class maintenanaceform(forms.ModelForm):
    class Meta:
        model=maintenance_payment 
        fields=["member_id","date_time","amount","month","description","payment_status"]
    