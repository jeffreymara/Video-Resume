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

from videoresume.models import User_Info, File, Company

def index(request):
    if request.user.is_authenticated():
        user = request.user


        ####PARAMETERS FOR FILE UPLOAD SIGNING####
        t = datetime.datetime.utcnow()
        dateStamp = t.strftime('%Y%m%d') #"20150830"
        regionName = "us-east-1"
        serviceName = "s3" #"iam"
        keyName = settings.AWS_SECRET_ACCESS_KEY #"wJalrXUtnFEMI/K7MDENG+bPxRfiCYEXAMPLEKEY"
        requestMethod = "POST" #"GET"
        host = 's3.amazonaws.com' #'iam.amazonaws.com'
        canonicalURI = "/"
        canonicalQueryString = "" #"Action=ListUsers&Version=2010-05-08"
        signingAlgorithm = "AWS4-HMAC-SHA256"
        requestParameters = ""
        xAmzDate = t.strftime('%Y%m%dT%H%M%SZ') #'20150830T123600Z'
        contentType = 'application/x-www-form-urlencoded; charset=utf-8'
        ###########################################

        post_policy = { "expiration": "2017-12-01T12:00:00.000Z",
                          "conditions": [
                            {"acl": "public-read" },
                            {"bucket": "resumehost" },
                            ["starts-with", "$key", ""],
                          ]
                        }
        hashedRequestPayload = hashlib.sha256(requestParameters.encode('utf-8')).hexdigest()

        canonicalRequest = requestMethod+"""
"""+canonicalURI+"""
"""+canonicalQueryString+"""
content-type:"""+contentType+"""
host:"""+host+"""
x-amz-date:"""+xAmzDate+"""

content-type;host;x-amz-date
"""+hashedRequestPayload

        hashedCanonicalRequest = hashlib.sha256(canonicalRequest.encode('utf-8')).hexdigest()
        #return HttpResponse(hashedCanonicalRequest)

        # This string to sign taken from: http://docs.amazonwebservices.com/amazonglacier/latest/dev/amazon-glacier-signing-requests.html#example-signature-calculation
        sts = signingAlgorithm+"""
"""+xAmzDate+"""
"""+dateStamp+"""/"""+regionName+"""/"""+serviceName+"""/aws4_request
"""+hashedCanonicalRequest

        def sign(key, msg):
            return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()

        def getSignatureKey(key, dateStamp, regionName, serviceName):
            kDate = sign(("AWS4" + key).encode("utf-8"), dateStamp)
            kRegion = sign(kDate, regionName)
            kService = sign(kRegion, serviceName)
            kSigning = sign(kService, "aws4_request")
            return kSigning

        signature = getSignatureKey(keyName, dateStamp, regionName, serviceName)
        signature = hmac.new(signature, sts.encode("utf-8"), hashlib.sha256).hexdigest()

        #return HttpResponse(signature)

        context_dict = {"signature_dict":{"x_amz_credential":settings.AWS_ACCESS_KEY_ID+"/"+dateStamp+"/"+regionName+"/"+serviceName+"/aws4_request",
                                            "post_policy":post_policy,
                                            "signature":signature},
                        "userinfo":user.user_info,
                        "video_resumes":user.user_info.file_set.filter(type="video resume").order_by('-date_created'),
                        "resumes":user.user_info.file_set.filter(type="resume").order_by('-date_created'),
                        "cover_letters":user.user_info.file_set.filter(type="cover letter").order_by('-date_created')}


        return render(request,"profile.html",context_dict)

    else:
        context_dict = {}
        return render(request,"index2.html",context_dict)

def sign_up(request):
    #context = RequestContext(request)
    context_dict = {}
    return render(request,"sign-up.html",context_dict)

def create_posting(request):
    #context = RequestContext(request)
    context_dict = {}
    return render(request,"create-posting.html",context_dict)

def talent(request):
    #context = RequestContext(request)
    candidate_list=[["Engineer - Data Analytics","Whatever tasks you end up taking on, you will have the opportunity to work with a skilled team of analysts as well as the flexibility to manage your own projects from design to launch. Your work will be used by engineers and product managers across the company, and you will help build a foundation for analytics at Slack."],
                    ["Engineer - Data Analytics","Whatever tasks you end up taking on, you will have the opportunity to work with a skilled team of analysts as well as the flexibility to manage your own projects from design to launch. Your work will be used by engineers and product managers across the company, and you will help build a foundation for analytics at Slack."],
                    ["Engineer - Data Analytics","Whatever tasks you end up taking on, you will have the opportunity to work with a skilled team of analysts as well as the flexibility to manage your own projects from design to launch. Your work will be used by engineers and product managers across the company, and you will help build a foundation for analytics at Slack."],
                    ["Engineer - Data Analytics","Whatever tasks you end up taking on, you will have the opportunity to work with a skilled team of analysts as well as the flexibility to manage your own projects from design to launch. Your work will be used by engineers and product managers across the company, and you will help build a foundation for analytics at Slack."],
                    ["Engineer - Data Analytics","Whatever tasks you end up taking on, you will have the opportunity to work with a skilled team of analysts as well as the flexibility to manage your own projects from design to launch. Your work will be used by engineers and product managers across the company, and you will help build a foundation for analytics at Slack."],
                    ["Engineer - Data Analytics","Whatever tasks you end up taking on, you will have the opportunity to work with a skilled team of analysts as well as the flexibility to manage your own projects from design to launch. Your work will be used by engineers and product managers across the company, and you will help build a foundation for analytics at Slack."],
                    ["Engineer - Data Analytics","Whatever tasks you end up taking on, you will have the opportunity to work with a skilled team of analysts as well as the flexibility to manage your own projects from design to launch. Your work will be used by engineers and product managers across the company, and you will help build a foundation for analytics at Slack."],
                    ["Engineer - Data Analytics","Whatever tasks you end up taking on, you will have the opportunity to work with a skilled team of analysts as well as the flexibility to manage your own projects from design to launch. Your work will be used by engineers and product managers across the company, and you will help build a foundation for analytics at Slack."],
                    ["Engineer - Data Analytics","Whatever tasks you end up taking on, you will have the opportunity to work with a skilled team of analysts as well as the flexibility to manage your own projects from design to launch. Your work will be used by engineers and product managers across the company, and you will help build a foundation for analytics at Slack."]]
    context_dict = {"posting_list":candidate_list,"page":"Positions"}
    return render(request,"talent.html",context_dict)

def companies(request):
    #context = RequestContext(request)
    company_list= Company.objects.all().order_by("-open_roles")
    context_dict = {"company_list":company_list}
    return render(request,"companies.html",context_dict)

def postings(request):
    #context = RequestContext(request)
    candidate_list=[["Company 1","Whatever tasks you end up taking on, you will have the opportunity to work with a skilled team of analysts as well as the flexibility to manage your own projects from design to launch. Your work will be used by engineers and product managers across the company, and you will help build a foundation for analytics at Slack."],
                    ["Company 2","Whatever tasks you end up taking on, you will have the opportunity to work with a skilled team of analysts as well as the flexibility to manage your own projects from design to launch. Your work will be used by engineers and product managers across the company, and you will help build a foundation for analytics at Slack."],
                    ["Company 3","Whatever tasks you end up taking on, you will have the opportunity to work with a skilled team of analysts as well as the flexibility to manage your own projects from design to launch. Your work will be used by engineers and product managers across the company, and you will help build a foundation for analytics at Slack."],
                    ["Company 4","Whatever tasks you end up taking on, you will have the opportunity to work with a skilled team of analysts as well as the flexibility to manage your own projects from design to launch. Your work will be used by engineers and product managers across the company, and you will help build a foundation for analytics at Slack."],
                    ["Company 5","Whatever tasks you end up taking on, you will have the opportunity to work with a skilled team of analysts as well as the flexibility to manage your own projects from design to launch. Your work will be used by engineers and product managers across the company, and you will help build a foundation for analytics at Slack."],
                    ["Company 6","Whatever tasks you end up taking on, you will have the opportunity to work with a skilled team of analysts as well as the flexibility to manage your own projects from design to launch. Your work will be used by engineers and product managers across the company, and you will help build a foundation for analytics at Slack."]]
    context_dict = {"posting_list":candidate_list,"page":"Companies"}
    return render(request,"talent.html",context_dict)

def posting(request):
    #context = RequestContext(request)
    candidate_list=[["Jack Mara","Associate","Founded companies in B2B and B2C spaces. Led product development, sales, strategy and raising efforts.  Hired and managed core team.","Founder / CEO 10Thoughts, Enterprise and B2C SaaS platform","Deloitte Consultant, State Street Corporate Strategy, Darden MBA","Sam Reynolds","Troy Smith"],
                    ["Brett Brohl","Associate","The goal is to build businesses with a team of great people, to have fun doing it, and to never stop learning new things.","Managing Director Techstars - Food + Tech","Founder: BoomBoom Prints, Easy Info, ScrubSquared Triumvirate Innovations","Susan Bode","Alan Apperman"],
                    ["Jerome Hughes","Associate","I love helping companies build new, innovative business units.  I have startup and Fortune 500 experience","Assistant Vice President Bank of America","Goldman Sachs Technology Analyst, Darden MBA","Samantha Lawrence","Julio Rey"],
                    ["Nathan Guo","Associate","I am passionate about commercializing emerging technologies and globalizing businesses","Parthenon-EY Consultant","Lux Capital Associate, Albemarle Process Engineer, Darden MBA","Tim Scott",""],
                    ["Joy Arcangeli","Associate","Passionate about improving education and working to give everyone the chance to succeed.","McKinsey Associate","Teach For All: Chief of Staff, Bain: Associate Consultant, Darden MBA","John Chou","Steve Smith"],
                    ["Andrew Higgins","Associate","History of exceeding sales goals at startups and large organizations in the tech space.","Sr. Account Executive Cloud Lock","Best of Boston, BostonCoach, Octagon","Troy Glenn",""],
                    ["Segre Amouzou","Associate","I work to help small, local business effectively reach customers and achieve their sales goals.","Founder and CEO: Delect","National Institute of Health, NanoTech ","Katie Allen",""],
                    ["Jeffrey Mara","Associate","Full-stack coder, experience building machine learning and AI capabilities for fast-growing, data intensive startups","Lockheed Martin: Engineer","Founder 10Thoughts, Department of Defense, NASA","Sam Webber","Todd Wilson"],
                    ["Sara Reed","Associate","I design websites, apps and marketing materials for consumer product companies seeking to better engage customers","Vice President Gillette","General Mills, HarrisTeeter, Rhode Island School of Design","Rick Smith",""]]
    context_dict = {"candidate_list":candidate_list}
    return render(request,"posting.html",context_dict)

def ajax(request):
    if request.method == 'POST':
        name = request.POST['name']
        if name == "create_account":
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            password = request.POST['password']
            screen_width = request.POST['screen_width']
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

            return HttpResponse(1)

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

    else:
        pass

