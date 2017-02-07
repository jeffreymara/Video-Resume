# -*- coding: utf-8 -*-
import datetime
import string
import random
import hmac
import hashlib
import base64

from django.conf import settings
from django.shortcuts import render,render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.core.mail import get_connection, EmailMultiAlternatives
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from videoresume.models import User_Info, File, Company, Blocked_Company, Job_Location, Role, Sub_Role

def profile(request):
    if request.user.is_authenticated():
        user = request.user
        if not user.user_info.submitted:
            return edit_profile(request,"personal-info")
        else:
            try:
                video_resume = user.user_info.file_set.filter(type="video resume").filter(uploaded=True).order_by('-date_created')[0]
            except:
                video_resume = ""
            try:
                resume = user.user_info.file_set.filter(type="resume").filter(uploaded=True).order_by('-date_created')[0]
            except:
                resume = ""
            context_dict = {"userinfo":get_user_info(request),
                            "video_resume": video_resume,
                            "resume": resume}
            return render(request,"profile.html",context_dict)
    else:
        return index(request)


def companies(request):
    context_dict = {"userinfo":get_user_info(request),}
    return render(request,"about_companies.html",context_dict)


def candidates(request):
    context_dict = {"userinfo":get_user_info(request),}
    return render(request,"candidates.html",context_dict)


def terms_and_conditions(request):
    context_dict = {"userinfo":get_user_info(request),}
    return render(request,"terms-and-conditions.html",context_dict)


def privacy_policy(request):
    context_dict = {"userinfo":get_user_info(request),}
    return render(request,"privacy-policy.html",context_dict)


def edit_profile(request,edit_profile_page="summary"):
     if request.user.is_authenticated():
        try:
            user = request.user
            userinfo = user.user_info
        except:
            logout(request)
            return index(request)
        if user.user_info.submitted:
            return profile(request)
        else:
            if userinfo.welcome_message:
                userinfo.welcome_message = False
                userinfo.save()
                show_welcome_message = "true"
            else:
                show_welcome_message = "false"

            try:
                video_resume = user.user_info.file_set.filter(type="video resume").filter(uploaded=True).order_by('-date_created')[0]
            except:
                video_resume = ""
            try:
                resume = user.user_info.file_set.filter(type="resume").filter(uploaded=True).order_by('-date_created')[0]
            except:
                resume = ""
            try:
                role = user.user_info.role_set.get()
            except:
                role = ""
            try:
                subroles = role.sub_role_set.all()
            except:
                subroles = ""
            if edit_profile_page == "personal-info":
                template_dict = {"title":"Step 1 of 7: Personal Info",
                                              "key":"personal-info",
                                              "content":"<table>\
                                                                 <tr><td>First Name<span class='required'>*</span></td><td><input type='text' name='first_name' value='"+userinfo.first_name+"' required/></td></tr>\
                                                                <tr><td>Last Name<span class='required'>*</span></td><td><input type='text' name='last_name' value='"+userinfo.last_name+"' required/></td></tr>\
                                                                <tr><td>Current Location<span class='required'>*</span></td><td><input type='text' name='location' value='"+userinfo.location+"' placeholder='City & State' required/></td></tr>\
                                                            </table>"}
            elif edit_profile_page == "resume":
                try:
                    resume = user.user_info.file_set.filter(type="resume").filter(uploaded=True).order_by('-date_created')[0]
                    resume_html = "<div class='resume_container'><div class='container-title'>Current Resume:</div><div class='resume_title'>" \
                                  "<a target='_blank' href='https://s3.amazonaws.com/resumehost/media/" \
                                  "uploads/"+resume.external_src+"."+resume.file_type+"'>"+resume.name+"</a></div>" \
                                  "<div class='resume_date'>Date uploaded: "+resume.date_created.strftime('%m/%d/%y')+"</div></div>"
                except:
                    resume_html = ""
                template_dict = {"title":"Step 4 of 6: Upload Your Resume",
                                       "key":"resume",
                                            "content":'\
                                                            <table>\
                                                                <tr>\
                                                                    <td>\
                                                                        Upload Resume (PDF)<span class="required">*</span>\
                                                                    </td>\
                                                                    <td>\
                                                                        <input type="file" />\
                                                                        <div class="progress"><div class="percentage"></div></div></div>\
                                                                    </td>\
                                                                    <td class="resume">\
                                                                        '+resume_html+'\
                                                                    </td>\
                                                                </tr>\
                                                                <tr>\
                                                                    <td>\
                                                                        LinkedIn URL\
                                                                    </td>\
                                                                    <td>\
                                                                        <input value="'+userinfo.linkedin_url+'" type="text" name="linkedin_url" placeholder="LinkedIn URL"/>\
                                                                    </td>\
                                                                </tr>\
                                                                <tr>\
                                                                    <td>\
                                                                        Personal Website\
                                                                    </td>\
                                                                    <td>\
                                                                        <input value="'+userinfo.personal_website_url+'" name="personal_website_url" type="text" placeholder="Website URL"/>\
                                                                    </td>\
                                                                </tr>\
                                                            </table>\
                                                        '}
            elif edit_profile_page == "summary":
                template_dict = {"title":"Step 1 of 6: Summary",
                                        "key":"summary",
                                         "content":"<div class='title'>Please briefly explain what you are looking for and what you have done.  This is your hook to get companies interested in viewing the rest of your profile! (50 words max)<span class='required'>*</span></div>\
                                                   <textarea name='summary'>"+userinfo.summary+"</textarea>"}
            elif edit_profile_page == "roles":
                role_dict = {" Marketing":"Brand Marketing,Product Marketing,Growth Hacker,PR / Communications,Content Marketing,Events Marketing,Email Marketing",
                             " Sales":"Account Executive,Account Manager,Business Development,Customer Success,Sales Manager,Sales Training",
                             " Product Management":"",
                             " Software Engineering":"Backend,Data,Engineering Manager,Frontend,Full Stack,Machine Learning,Mobile,UX,Security",
                             " Data Science":"Data Analyst,Data Scientist",
                             " Human Resource":"Recruiter, People Ops",
                             " Finance Operations":"Accounting,Financial Analysis,General Management,Office Manager",
                             " Design":"Graphic Designer,Product Designer,UX Designer",
                             "Other":""}
                role_html = "<tr>"
                col_count = 1
                for key in sorted(role_dict):
                    if role:
                        if key == role.name:
                            class_string = "class='selected'"
                        else:
                            class_string = "class=''"
                    else:
                        class_string = ""
                    role_html += "<td "+class_string+" data-subroles='"+role_dict[key]+"'>"+key+"</td>"

                    if col_count == 3:
                        col_count = 1
                        role_html+= "</tr><tr>"
                    else:
                        col_count += 1
                role_html += "</tr>"

                subrole_html = "<tr>"
                col_count = 1
                if role:
                    if role_dict[role.name]:
                        col_count = 1
                        for sr2 in role_dict[role.name].split(","):
                            success = False
                            for sr1 in subroles:
                                if sr1.name == sr2:
                                    success = True
                            if success:
                                class_string = "class='selected'"
                            else:
                                class_string = ""
                            subrole_html += "<td "+class_string+">"+sr2+"</td>"
                            if col_count == 3:
                                col_count = 1
                                subrole_html+= "</tr><tr>"
                            else:
                                col_count += 1
                        subrole_html += "</tr>"
                        subrole_title_html = "<div class='title title-remove'>What role(s) are you currently seeking?</div>"

                    else:
                        if role.name == "Other":
                            subrole_title_html = "<div class='title title-remove'>What is your desired career?</div>"
                            try:
                                val = subroles[0].name
                            except:
                                val = ""
                            subrole_html = "<input class='title-remove' type='text' value='"+val+"' placeholder='Desired career'/>"

                        else:
                            subrole_html = ""
                            subrole_title_html = ""
                else:
                    subrole_html = ""
                    subrole_title_html = ""


                template_dict = {"title":"Step 2 of 6: Roles",
                                      "key":"roles",
                                         "content":"<div class='title'>What career are you currently seeking? (Choose 1)<span class='required'>*</span></div><table class='roles mainroles'>"
                                                   +role_html+
                                                   "</table>"+subrole_title_html+
                                                   "<table class='roles subroles'>"+subrole_html+"</table>"}
            elif edit_profile_page == "job-preferences":

                locations = user.user_info.job_location_set.all()
                li_html = ""
                location_list = ["Boston","New York","San Francisco","Twin Cities"]
                for location in location_list:
                    if len(locations.filter(name=location)):
                        li_html+="<li><input type='checkbox' checked name='"+location+"'/>"+location+"</li>"
                    else:
                        li_html+="<li><input type='checkbox' name='"+location+"'/>"+location+"</li>"



                template_dict = {"title":"Step 3 of 6: Locations",
                                                "key":"job-preferences",
                                         "content":"<div class='title'>What location(s) are you willing to work in? (Provide at least 1)<span class='required'>*</span></div><ol class='list-add'>"+li_html+\
                                                   "</ol>"}
            elif edit_profile_page == "video-resume":
                try:
                    resume_html = "<div class='resume_container'><div class='container-title'>Current Video Resume:</div><div class='resume_title'>" \
                                  "<a target='_blank' href='https://s3.amazonaws.com/resumehost/media/" \
                                  "uploads/"+video_resume.external_src+"."+video_resume.file_type+"'>"+video_resume.name+"</a></div>" \
                                  "<div class='resume_date'>Date uploaded: "+video_resume.date_created.strftime('%m/%d/%y')+"</div></div>"
                except:
                    resume_html = ""
                template_dict = {"title":"Step 5 of 6: Upload video answer to one question (below)<br /><br />Candidates with a video pitch are 8x more likely to receive interviews",
                                             "key":"video-resume",
                                            "content":'<table>'
                                            '<tr><td></td><td></td><td class="resume">'+resume_html+'</td></tr>'
                                                      '<tr>'
                                                      '<td style="width: 15%;">'
                                                      'Upload Video Pitch (video file)<span class="required">*</span>'
                                                      '</td>'
                                                      '<td style="width: 50%;">'
                                                      '<input type="file" required/>'
                                                      '</td>'
                                                    '<td style="width: 35%; padding-left: 30px;">'
                                                        '<div class="resume-list-title">Answer <u>ONE</u> of the following questions on video in 90 seconds or less</div>'
                                                        '<ul class="resume-list">'
                                                        '<li>What is your biggest accomplishment?</li>'
                                                        '<li>Why are you ideal for the career you selected?</li>'
                                                        '<li>Why should people want to work with you?</li></ul>'
                                                        '</td>'
                                                    '</tr>'
                                                    '<tr><td>'
                                                    '</td>'
                                                    '<td>'
                                                    '<div class="resume-list-title">Video Pitch Checklist</div>'
                                                        '<ul class="resume-list"><li>90 seconds is the ideal length for a video pitch</li>'
                                                        '<li>Use the camera on your computer or phone</li>'
                                                        '<li>Dress business casual</li>'
                                                        '<li>Look directly into the camera</li>'
                                                        '<li>Try to keep the light in front of you, not behind you</li></ul>'
                                                        '</td>'
                                                    '</td>'
                                                    '</table>'}
            elif edit_profile_page == "submit":
                missing_html = "<li>Before submitting, please provide your:</li>"
                complete = True
                if not user.user_info.first_name:
                    missing_html += "<a href='/edit-profile/personal-info/'><li>First Name</li></a>"
                    complete = False
                if not user.user_info.last_name:
                    missing_html += "<a href='/edit-profile/personal-info/'><li>Last Name</li></a>"
                    complete = False

                if not user.user_info.summary:
                    missing_html += "<a href='/edit-profile/summary/'><li>Summary</li></a>"
                    complete = False

                if not user.user_info.role_set.all():
                    missing_html += "<a href='/edit-profile/roles/'><li>Desired Roles</li></a>"
                    complete = False
                if not user.user_info.job_location_set.all():
                    missing_html += "<a href='/edit-profile/job-preferences/'><li>Job Location Preferences</li></a>"
                    complete = False

                if not resume:
                    missing_html += "<a href='/edit-profile/resume/'><li>Resume</li></a>"
                    complete = False

                if not video_resume:
                    missing_html += "<a href='/edit-profile/video-resume/'><li>Video Pitch</li></a>"
                    complete = False

                if complete:
                    missing_html = ""
                    complete_class = "complete"

                else:
                    complete_class = "not_complete"

                blocked_companies = user.user_info.blocked_company_set.all()
                extra_li = 3 - len(blocked_companies)
                li_html = ""

                c = 0
                for company in blocked_companies:
                    if c == 0:
                        fa_times = ""
                    else:
                        fa_times = "<i class='fa fa-times'></i>"

                    li_html+="<li><input value='"+company.name+"' placeholder='Company Name'/>"+fa_times+"</li>"
                    c+=1

                while extra_li > 0:
                    if c == 0:
                        fa_times = ""
                    else:
                        fa_times = "<i class='fa fa-times'></i>"

                    li_html+="<li><input placeholder='Company Name'/>"+fa_times+"</li>"
                    extra_li -= 1

                    c+=1

                template_dict = {"title":"Step 6 of 6: Submit",
                                                  "key":"submit",
                                         "content":"<ul class='missing'>"+missing_html+"\
                                                   </ul>"+"<div class='title'>(Optional) Block Companies: Any employers listed here will not be able to search for or view your profile - some candidates choose to block their current employer</div><ol class='list-add'>"+li_html+"</ol><div class='add-li'>+ Another Company</div>",
                                         "complete":complete_class}

            context_dict = {"template_dict":template_dict,
                            "userinfo":user.user_info,
                            "resume":resume,
                            "video_resume":video_resume,
                            "role":role,
                            "subroles":subroles,
                            "locations":user.user_info.job_location_set.all(),
                            "show_welcome_message":show_welcome_message,
                            "cover_letters":user.user_info.file_set.filter(type="cover letter").order_by('-date_created'),
                            "edit_profile_page":edit_profile_page
                            }
            return render(request,"edit-profile.html",context_dict)
     else:
         return index(request)


#def index(request):
#    context_dict = {"userinfo":get_user_info(request)}
#    return render(request,"index2.html",context_dict)

def sign_up(request):
    #context = RequestContext(request)
    context_dict = {}
    return render(request,"sign-up.html",context_dict)

def create_posting(request):
    #context = RequestContext(request)
    context_dict = {}
    return render(request,"create-posting.html",context_dict)

def index(request):
    #context = RequestContext(request)
    company_list = Company.objects.all().order_by("-open_roles")
    context_dict = {"company_list": company_list,"userinfo":get_user_info(request)}
    return render(request,"companies.html",context_dict)

def ajax(request):
    if request.method == 'POST':
        name = request.POST['name']
        if name == "create_account":
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            password = request.POST['password']
            screen_width = request.POST['screen_width']
            if len(User.objects.filter(email=email)):
                return HttpResponse("duplicate")
            else:
                new_user = User.objects.create_user(email, email, password)
                new_user.first_name = first_name
                new_user.last_name = last_name
                new_user.save()

                new_user_info = User_Info(first_name = first_name,
                                            last_name = last_name,
                                            email = email,
                                            user_type = "employee",
                                            verification = ''.join(random.choice(string.ascii_uppercase) for i in range(64)),
                                            screen_width = int(screen_width),
                                            user_id = new_user)
                new_user_info.save()

                user = authenticate(username=new_user.username, password=password)
                login(request, user)
                return HttpResponse("success")

        elif name == "log_in":
            logout(request)
            email = request.POST['email']
            password = request.POST['password']
            match = "email_not_registered"
            if len(User.objects.filter(email=email)):
                account = User.objects.get(email=email)
                user = authenticate(username=account.username, password=password)
                match = "success"
                if user is not None:
                    #if account_from_db.verification == "verified":
                        login(request, user)
                        return HttpResponse(match)
                        """else:
                        fn = account_from_db.first_name
                        ln = account_from_db.last_name
                        verify = account_from_db.verification

                        sender = '10Thoughts <donotreply@10thoughts.com>'
                        connection = get_connection()
                        connection.open()
                        html_content = 'Hello '+fn+' '+ln+ ' welcome to 10Thoughts! Please verify your email by clicking this link <a href="http://www.10thoughts.com/'+account_from_db.url+'/login/?type=verify&id='+verify+'&email='+email+'">http://www.10thoughts.com/'+account_from_db.url+'/login/?type=verify&id='+verify+'&email='+email+'</a>'
                        text_content = 'Hello '+fn+' '+ln+ ' welcome to 10Thoughts! Please verify your email by clicking this link http://www.10thoughts.com/'+account_from_db.url+'/login/?type=verify&id='+verify+'&email='+email
                        msg = EmailMultiAlternatives("10Thoughts Verification", text_content,sender, [email], connection=connection)
                        msg.attach_alternative(html_content, "text/html")
                        msg.send()
                        match = "unverified"
                        return HttpResponse(match)"""
                else:
                    match = 0
                    return HttpResponse(match)
            else: #user does not exist
                match = 0
                return HttpResponse(match)

        elif name == "upload":
            try:
                if request.user.is_authenticated():
                    user = request.user
                    userinfo = user.user_info
                    file_name = request.POST['file_name']
                    type = request.POST['type']
                    file_type = request.POST['file_type']
                    size = request.POST['size']
                    file_upload = File(name=file_name,user_id=userinfo,type=type,file_type=file_type,size=int(size))
                    file_upload.save()
                    return HttpResponse("success")
                else:
                    pass
            except Exception as e:
                return HttpResponse(e)

        elif name == "delete_file":
            if request.user.is_authenticated():
                user = request.user
                file_id = request.POST['file_id']
                file = user.user_info.file_set.get(id=file_id)
                file.delete()
                return HttpResponse("success")
            else:
                pass
        elif name == "logout":
            logout(request)
            return HttpResponse("success")

        elif name == "personal-info":
            if request.user.is_authenticated():
                user = request.user
                user.user_info.first_name = request.POST["first_name"]
                user.user_info.last_name = request.POST["last_name"]
                user.user_info.location = request.POST["location"]
                user.user_info.phone_number = request.POST["phone_number"]
                user.user_info.save()



                return HttpResponse("success")

        elif name == "summary":
            if request.user.is_authenticated():
                user = request.user
                user.user_info.summary = request.POST["summary"]
                user.user_info.save()
                return HttpResponse("success")

        elif name == "resume":
            if request.user.is_authenticated():
                user = request.user
                if 'linkedin_url' in request.POST:
                    user.user_info.linkedin_url = request.POST['linkedin_url']
                    user.user_info.personal_website_url = request.POST['personal_website_url']
                    user.user_info.save()

                    if not 'file_name' in request.POST:
                        return HttpResponse("success")

                if 'file_name' in request.POST:
                    file_name = request.POST['file_name']
                    type = request.POST['type']
                    file_type = request.POST['file_type']
                    size = request.POST['size']
                    file_upload = File(name=file_name,user_id=user.user_info,type=type,file_type=file_type,size=int(size))
                    file_upload.save()
                    external_src = settings.AWS_FILENAME_ROOT+type+"-"+str(file_upload.id)+''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
                    file_upload.external_src = external_src
                    file_upload.save()
                    return HttpResponse(external_src)

        elif name == "verify-upload":
            if request.user.is_authenticated():
                user = request.user
                external_src = request.POST['external_src']
                file = user.user_info.file_set.filter(external_src=external_src).get()
                file.uploaded = True
                file.save()
                return HttpResponse("success")

        elif name == "roles":
            if request.user.is_authenticated():
                user = request.user
                try:
                    role = user.user_info.role_set.get()
                    subroles = role.sub_role_set.all()
                    role.delete()
                    subroles.delete()
                except:
                    pass

                for role in request.POST["roles"].split("***"):
                    if role:
                        new_role = Role(name=role,user_id=user.user_info)
                        new_role.save()
                        for subrole in request.POST["subroles"].split("***"):
                            if subrole:
                                new_sub_role = Sub_Role(name=subrole,role_id=new_role)
                                new_sub_role.save()

                return HttpResponse("success")

        elif name == "location":
            if request.user.is_authenticated():
                user = request.user
                job_locations = user.user_info.job_location_set.all()
                job_locations.delete()

                for location in request.POST["location_list"].split("***"):
                    if location:
                        job_location = Job_Location(name=location,user_id=user.user_info)
                        job_location.save()

                return HttpResponse("success")

        elif name == "submit-application":
            if request.user.is_authenticated():
                user = request.user
                user.user_info.submitted = True
                user.user_info.save()

                blocked_companies = user.user_info.blocked_company_set.all()
                blocked_companies.delete()

                for company in request.POST["company_list"].split("***"):
                    if company:
                        blocked_company = Blocked_Company(name=company,user_id=user.user_info)
                        blocked_company.save()

                return HttpResponse("success")

        elif name == "load-companies":
            company_index = int(request.POST["company_index"])
            company_list = Company.objects.filter(open_roles__lte=company_index).order_by("-open_roles")[1:7]
            company_html = ''
            for company in company_list:
                company_html += ' <div class="talent-container" data-roles="'+str(company.open_roles)+'">'\
                                '<div class="video_description">'+company.video_description+'</div>'\
                                '<div class="name"><img src="'+company.profile_image_external+'"/> <div class="text">'+company.name+'</div></div>'\
                            '</div>'

            return HttpResponse(company_html)

        elif name == "help":
            if request.user.is_authenticated():
                user = request.user
                user.user_info.help_requested = True
                user.user_info.save()
                return HttpResponse("success")

    else:
        pass

def get_user_info(request):
    if request.user.is_authenticated():
        user = request.user
        userinfo = user.user_info
    else:
        userinfo = ""
    return userinfo

