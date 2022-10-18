import email
from urllib import response
from django.shortcuts import render
from .models import Profile
import pdfkit
from django.http import HttpResponse
from django.template import loader
import io
# Create your views here.
def accept(request):
    if request.method == "POST":
        name = request.POST.get("name","")
        email = request.POST.get("email","")
        phone = request.POST.get("phone","")
        summary = request.POST.get("summary","")
        school = request.POST.get("school","")
        university = request.POST.get("university","")
        previous_work = request.POST.get("previous_work","")
        skills = request.POST.get("skills","")
        profile = Profile(name=name,email=email,phone=phone,summary = summary,school=school,university=university,previous_work=previous_work,skills=skills)
        profile.save()
    return render(request,'pdf/accept.html')

def resume(request,id): #include id becuase we want to download of specific person 
    user_profile=Profile.objects.get(pk = id)
    template = loader.get_template('pdf/resume.html') #to store it in a variable,it will be empty since it will not have context
    #creating the html string to pass onto the library of pdfkit
    html = template.render({'user_profile':user_profile}) #passing the context
    #using this since we need to pass this to the pdf kit library
    #.string method converts string from html and convert it to pdf file
    options={
        'page-size':'Letter',
        'encoding' : 'UTF-8',
    }
    pdf = pdfkit.from_string(html,False,options) #here the html file is converted into pdf
    #Now to make it downloadable
    response = HttpResponse(pdf,conten_type='application/pdf')
    response['Content-Disposition'] = 'attachment'
    filename = 'resume.pdf'
    return response
    # return render(request,'pdf/resume.html',{'user_profile':user_profile}) -->Initially used to check all details

def list(request):
    profiles = Profile.objects.all()
    return render(request,'pdf/list.html',{'profiles':profiles})
