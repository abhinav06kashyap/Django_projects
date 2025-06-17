from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
#calling models/tables to push or get data from
from Application_Form.models import credentials, applications
import random
from django.db import connection
from django.core.mail import EmailMessage

#function to generate unique id        
def unique_id():
    pass_constrains = "abcdefghijklmnopqrstuvwxyz1234567890@$*ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    u_id=""
    i=8
    while i != 0:
        u_id += random.choice(pass_constrains)
        i-=1
    return u_id

#function to generate OTP        
def otp_gen():
    pass_constrains = "1234567890"
    u_id=""
    i=6
    while i != 0:
        u_id += random.choice(pass_constrains)
        i-=1
    return u_id

# this function is linked to the landing page and will take you to login/startup page
def landing_page(request):
    try:
        if request.method == 'POST':
            if request.POST.get('log_btn'):
                return redirect('login_page')
            elif request.POST.get('new_btn'):
                return redirect('signup')
        else:
            pass
    except:
        messages.add_message(request, messages.ERROR, "Unexpected Error.")
    return render(request,"Main/landing_page.html")

def login_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        p_word = request.POST.get('p_word')
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM APPLICATION_FORM_CREDENTIALS WHERE Email = '{email}';")
            user_item = cursor.fetchone()
        if user_item:
            if p_word == user_item[2]:
                u_id = user_item[0]
                with connection.cursor() as cursor:
                    cursor.execute(f"SELECT * FROM APPLICATION_FORM_APPLICATIONS WHERE Email = '{email}';")
                    user_item = cursor.fetchone()
                if user_item:
                    url = '/exist_user/?u_id={}'.format(u_id)
                    return HttpResponseRedirect(url)
                else:
                    url = '/new_user/?u_id={}'.format(u_id)
                    return HttpResponseRedirect(url)
            else:
                messages.add_message(request, messages.ERROR, "Wrong email/password.")
        else:    
            messages.add_message(request, messages.ERROR, f"{email} is not regestered. Sign-up to fill application.")
    return render(request, 'Main/login.html')

#this fuction will get user signup and generate a unique if for them
def signup(request):
    try:
        if request.method == 'POST':
            if request.POST.get('signup'):
                email = request.POST.get('email')
                p_word = request.POST.get('p_word')
                if "@gmail.com" in email:
                    if ' ' not in p_word:
                        with connection.cursor() as cursor:
                            cursor.execute(f"SELECT * FROM APPLICATION_FORM_CREDENTIALS WHERE Email = '{email}';")
                            row = cursor.fetchone()
                        if row:
                            messages.add_message(request, messages.ERROR, f"{email} is already registered.")
                        else:
                            #genrating unique student id 
                            u_id = unique_id()
                            
                            #authenticate user with an OTP over mail
                            try:
                                otp = otp_gen()
                                mail = EmailMessage('OTP verification for AKU', 
                                                    f'Hi student, your OTP is {otp}. It is valid for next 10 mins.',
                                                    to=[email])
                                mail.send()
                                return render(request, 'Main/signup.html',{'u_id':u_id, 'otp':otp,'email':email,'p_word':p_word})
                            except:
                                messages.add_message(request, messages.ERROR, "Error sending OTP to given email try again after sometime.")
                    else:
                        messages.add_message(request, messages.ERROR, "Password must not contain blank spaces, try again.")
                else:    
                    messages.add_message(request, messages.ERROR, "We only accept emails with @gmail.com domain")
            elif request.POST.get('OTP'):
                user_otp = request.POST.get('u_otp')
                u_data = request.POST.get('OTP').split(' ')
                print(u_data)
                u_id = u_data[0]
                sent_otp = u_data[1]
                email = u_data[2]
                p_word = u_data[3]
                if user_otp == sent_otp:
                    #insert data in mysql
                    data = credentials(U_ID=u_id,Email=email,Password=p_word)
                    data.save()
                    
                    #send Emmail to new user
                    email = EmailMessage('AKU account created successfully', 
                                        'Hi student, your account is created. Welcome to AKU, for any query you can mail to our founder Abhinav Kashyap (kashyap06abhinav@gmail.com).\n\nBest Regards\nA.K.U',
                                        to=[email])
                    email.send()
                    
                    # create url to redirect to next page
                    url="/new_user/?u_id={}".format(u_id)
                    return HttpResponseRedirect(url)
                else:
                    messages.add_message(request, messages.ERROR, "Verification otp is incorrect.")
    except:
        messages.add_message(request, messages.ERROR, "Unexpected Error")
    return render(request, 'Main/signup.html')

#this function allows you to register a new user
def new_user(request):
    try:
        if request.method == 'POST':
            u_id = request.POST.get('u-id')
            if u_id:
                url = "/Application_Form/?u_id={}".format(u_id)
                return HttpResponseRedirect(url)
            else:
                messages.add_message(request, messages.ERROR, "Error, try again.")
        else:
            u_id = request.GET.get('u_id')
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT * FROM APPLICATION_FORM_CREDENTIALS WHERE U_ID = '{u_id}';")
                row = cursor.fetchone()
            mail = row[1] 
    except:
        messages.add_message(request, messages.ERROR, "Unexpected error.") 
    return render(request, 'Main/home_page.html', {'mail':mail,'ID':u_id})

# this function is to take user to edit the appliction or view.
def exist_user(request):
    try:
        if request.method == 'POST':
            u_id = request.POST.get('u-id')
            if "exist_form" in request.POST:
                url = "/view_exist_form/?u_id={}".format(u_id)
                return HttpResponseRedirect(url)
            elif "edit_form" in request.POST:
                url = "/edit_form/?u_id={}".format(u_id)
                return HttpResponseRedirect(url)
        else:
            u_id = request.GET.get('u_id')
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT * FROM APPLICATION_FORM_CREDENTIALS WHERE U_ID = '{u_id}';")
                row = cursor.fetchone()
            mail = row[1]
    except:
        messages.add_message(request, messages.ERROR, "Unexpected error.") 
    return render(request, 'Main/home_page.html', {'mail':mail,'ID':u_id, "exist":"yes"})

#this fucntion will help update user password
def change_password(request):
    try:
        if request.method == 'POST':
            email = request.POST.get('email')
            old_pass = request.POST.get('old_p_word')
            new_pass = request.POST.get('new_p_word')
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT * FROM APPLICATION_FORM_CREDENTIALS WHERE Email = '{email}' and Password = '{old_pass}';")
                row = cursor.fetchone()
            u_id = row[0] 
            curr_user = row[3]
            data = credentials(U_ID=u_id,Email=email,Password=new_pass,id=curr_user)
            data.save()
            messages.add_message(request, messages.INFO, "Password changed.")
            return redirect('login_page')
    except:
        messages.add_message(request, messages.ERROR, "You are not registered or old password didn't match") 
    return render(request, 'Main/password_change.html')

#this is to present the application form and call welcome page function.
def application_form(request):
    try:   
        if request.method == 'POST':
            if request.POST.get('back'):
                u_id = request.POST.get('back')
                with connection.cursor() as cursor:
                    cursor.execute(f"SELECT * FROM APPLICATION_FORM_APPLICATIONS WHERE U_ID = '{u_id}'")
                    row = cursor.fetchone()
                if row:
                    url="/exist_user/?u_id={}".format(u_id)
                    return HttpResponseRedirect(url)
                else:
                    url="/new_user/?u_id={}".format(u_id)
                    return HttpResponseRedirect(url)
            else:
                u_id = request.POST.get('unique_id')
                f_name = request.POST.get("f_name")
                l_name = request.POST.get("l_name")
                fandg_name = request.POST.get("fandg_name")
                gender = request.POST.get("gen")
                email = request.POST.get('email')
                phone = request.POST.get("phone")
                course = request.POST.get("course")
                b_date = request.POST.get("b_date")
                #insert data in mysql
                query = applications(U_ID=u_id, F_name=f_name, L_name=l_name, FandG_name=fandg_name, Gen=gender, Email=email, Ph=phone, Course=course, B_date=b_date)
                query.save()
                
                # send a email confirmation of application submitted
                mail = EmailMessage('A.K.U Application Form', 
                                        f"""Hi {f_name+" "+l_name}, your application form is submitted successfully. We will review it and contact you shortly, for any query you can mail to our founder Abhinav Kashyap (kashyap06abhinav@gmail.com).\n\n\n
Details:-\n
Unique ID* : {u_id}\n
First name* : {f_name}\n
Last name : {l_name}\n
Father or Gaurdian Name* : {fandg_name}\n
Gender : {gender}\n
E-Mail* : {email}\n
Phone* : {phone}\n
Course* : {course}\n
Birth Date* : {b_date}\n\n
Best Regards\nA.K.U""",
                                        to=[email])
                mail.send()
                
                url = "view_form/?u_id={}".format(u_id)
                return HttpResponseRedirect(url)
        else:
            u_id = request.GET.get('u_id')
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT * FROM APPLICATION_FORM_CREDENTIALS WHERE U_ID = '{u_id}';")
                row = cursor.fetchone()
            email = row[1] 
    except:
        messages.add_message(request, messages.ERROR, "Unexpected error.") 
    return render(request, 'Application/application_form.html',{'U_ID':u_id,'st_mail':email})

#this function allows user to edit the existing application
def edit_form(request):
    try:   
        if request.method == 'POST':
            if request.POST.get('back'):
                u_id = request.POST.get('back')
                url="/exist_user/?u_id={}".format(u_id)
                return HttpResponseRedirect(url)
            else:
                u_id = request.POST.get('unique_id')
                f_name = request.POST.get("f_name")
                l_name = request.POST.get("l_name")
                fandg_name = request.POST.get("fandg_name")
                gender = request.POST.get("gen")
                email = request.POST.get('email')
                phone = request.POST.get("phone")
                course = request.POST.get("course")
                b_date = request.POST.get("b_date")
                with connection.cursor() as cursor:
                    cursor.execute(f"SELECT * FROM APPLICATION_FORM_APPLICATIONS WHERE U_ID = '{u_id}';")
                    row = cursor.fetchone()
                prime_id = row[9] 
                
                #insert data in mysql
                query = applications(U_ID=u_id, F_name=f_name, L_name=l_name, FandG_name=fandg_name, Gen=gender, Email=email, Ph=phone, Course=course, B_date=b_date, id = prime_id)
                query.save()
                
                # send a email confirmation of application submitted
                mail = EmailMessage('A.K.U Application Form', 
                                        f"""Hi {f_name+" "+l_name}, your application is edited successfully. We will review it and contact you shortly, for any query you can mail to our founder Abhinav Kashyap (kashyap06abhinav@gmail.com).\n\n\n
Details:-\n
Unique ID* : {u_id}\n
First name* : {f_name}\n
Last name : {l_name}\n
Father or Gaurdian Name* : {fandg_name}\n
Gender : {gender}\n
E-Mail* : {email}\n
Phone* : {phone}\n
Course* : {course}\n
Birth Date* : {b_date}\n\n
Best Regards\nA.K.U""",
                                        to=[email])
                mail.send()
                
                url = "/Application_Form/view_form/?u_id={}".format(u_id)
                return HttpResponseRedirect(url)
        else:
            u_id = request.GET.get('u_id')
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT * FROM APPLICATION_FORM_APPLICATIONS WHERE U_ID = '{u_id}';")
                row = cursor.fetchone()
            f_name = row[1]
            l_name = row[2]
            fandg_name = row[3]
            gender = row[4]
            email = row[5]
            phone = row[6]
            course = row[7]
            b_date = row[8]
    except:
        messages.add_message(request, messages.ERROR, "Unexpected error.") 
        return render(request, 'Main/home_page.html')
    return render(request, 'Application/application_form.html',{'U_ID':u_id,'f_n':f_name,'l_n':l_name,'f_g_n':fandg_name,'gen':gender,'st_mail':email,'ph':phone,'course':course,'b_d':b_date})

#this will present the welcome page after we click submit on application form
def view_form(request):
    if request.method == 'POST':
        u_id = request.POST.get('back')
        url="/exist_user/?u_id={}".format(u_id)
        return HttpResponseRedirect(url)
    if request.method == 'GET':
        u_id = request.GET.get('u_id')
        with connection.cursor() as cursor:
                cursor.execute(f"SELECT * FROM APPLICATION_FORM_APPLICATIONS WHERE U_ID = '{u_id}';")
                row = cursor.fetchone()
        f_name = row[1]
        l_name = row[2]
        fandg_name = row[3]
        gender = row[4]
        email = row[5]
        phone = row[6]
        course = row[7]
        b_date = row[8]
    return render(request, "Application/application_submit.html",{'U_ID':u_id,'f_n':f_name,'l_n':l_name,'f_g_n':fandg_name,'gen':gender,'mail':email,'ph':phone,'course':course,'b_d':b_date})

#this function will present the existing application to user.
def view_exist_form(request):
    if request.method == 'POST':
        u_id = request.POST.get('back')
        url="/exist_user/?u_id={}".format(u_id)
        return HttpResponseRedirect(url)
    if request.method == 'GET':
        u_id = request.GET.get('u_id')
        with connection.cursor() as cursor:
                cursor.execute(f"SELECT * FROM APPLICATION_FORM_APPLICATIONS WHERE U_ID = '{u_id}';")
                row = cursor.fetchone()
        f_name = row[1]
        l_name = row[2]
        fandg_name = row[3]
        gender = row[4]
        email = row[5]
        phone = row[6]
        course = row[7]
        b_date = row[8]
    return render(request, "Application/application_submit.html",{'U_ID':u_id,'f_n':f_name,'l_n':l_name,'f_g_n':fandg_name,'gen':gender,'mail':email,'ph':phone,'course':course,'b_d':b_date,'exist':'yes'})
    