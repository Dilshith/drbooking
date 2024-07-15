from datetime import datetime

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from django.db.models.functions import datetime
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.

from DoctorBooking.models import *


#LOGIN

def login(request):
    return render(request, 'Login.html')

def logincode(request):
    uname = request.POST['textfield']
    pswrd = request.POST['textfield2']
    try:
        ob = login_table.objects.get(username = uname, password = pswrd)

        if ob.type == 'admin':
            ob1=auth.authenticate(username='admin',password='admin')
            if ob1 is not None:
                auth.login(request,ob1)
            request.session['lid'] = ob.id
            return HttpResponse('''<script> alert("Success"); window.location = "/admin_view"</script>''')
        elif ob.type =='user':
            ob1=auth.authenticate(username='admin', password = 'admin')
            if ob1 is not None:
                auth.login(request,ob1)
            request.session["lid"] = ob.id
            return HttpResponse('''<script> alert("welcome user"); window.location = "/user_homePage"</script>''')

        elif ob.type == 'doctor':
            ob1=auth.authenticate(username='admin', password='admin')
            if ob1 is not None:
                auth.login(request,ob1)
            request.session["lid"] = ob.id
            return HttpResponse('''<script> alert("welcome doctor"); window.location = "/doctor_homePage"</script>''')
        elif ob.type == 'pending':

            return HttpResponse('''<script>alert("Admin should accept you first"); window.location="/"</script>''')
        else:
            return HttpResponse ('''<script>alert("Invalid user"); window.location="/"</script>''')
    except:
        return HttpResponse('''<script>alert("Invalid user"); window.location="/"</script>''')




def new_registrationDoctor(request):
    return render(request,'DOCTOR/docRegistration.html')

def doc_registrationCode(request):
    name = request.POST['textfield2']
    image = request.FILES['file']
    fs = FileSystemStorage()
    fsave = fs.save(image.name, image)
    Designation = request.POST['textfield4']
    email = request.POST['textfield3']
    experience = request.POST['textfield5']
    place = request.POST['textfield32']
    pin = request.POST['textfield33']
    post = request.POST['textfield34']
    phone = request.POST['textfield35']
    username = request.POST['textfield36']
    password = request.POST['textfield37']


    ob = login_table()
    ob.username = username
    ob.password= password
    ob.type = "pending"
    ob.save()


    orr = doctor_reg_table()
    orr.LOGIN=ob
    orr.name = name
    orr.image = fsave
    orr.Designation = Designation
    orr.email = email
    orr.experience = experience
    orr.place= place
    orr.pin = pin
    orr.post = post
    orr.phone = phone
    orr.save()

    return HttpResponse('''<script> alert ("Success"); window.location="/"</script>''')

def new_registrationUser(request):
    return render(request,'USER/User registration.html')

def user_registrationCode(request):
    name = request.POST['textfield2']
    image = request.FILES['file']
    fs = FileSystemStorage()
    fsave = fs.save(image.name, image)
    email = request.POST['textfield3']
    place = request.POST['textfield32']
    pin = request.POST['textfield33']
    post = request.POST['textfield34']
    phone = request.POST['textfield35']
    username = request.POST['textfield36']
    password = request.POST['textfield37']

    ob = login_table()
    ob.username = username
    ob.password = password
    ob.type = "pending"
    ob.save()


    orr = user_reg_table()
    orr.LOGIN =ob
    orr.name = name
    orr.image = fsave
    orr.email = email
    orr.place = place
    orr.pin = pin
    orr.post = post
    orr.phone = phone
    orr.save()

    return HttpResponse('''<script> alert ("Success"); window.location="/"</script>''')

#ADMIN

@login_required(login_url='/')

def admin_view(request):
    return render(request,'ADMIN/admin view.html')

@login_required(login_url='/')
def admin_view_doctors(request):
    dr = doctor_reg_table.objects.all()
    return render(request,'ADMIN/verify doctor.html',{'dr':dr})

@login_required(login_url='/')
def admin_acceptDoctor(request,lid):
    ob = login_table.objects.get(id = lid)
    ob.type = "doctor"
    ob.save()
    return HttpResponse('''<script> alert("Accepted!");window.location="/admin_view_doctors"</script>''')

@login_required(login_url='/')
def admin_rejectDoctor(request,lid):
    ob = login_table.objects.get(id=lid)
    ob.type = "Rejected"
    ob.save()
    return HttpResponse('''<script> alert("Rejected!"); window.location = "/admin_view_doctors"</script>''')

@login_required(login_url='/')
def admin_searchDoctor(request):
    name = request.POST['textfield']
    phone = request.POST['textfield']
    # ob = doctor_reg_table.objects.filter(name__icontains= name,phone=phone)

    ob = doctor_reg_table.objects.filter(
        Q(name__icontains=name) | Q(phone__icontains=phone)
    )

    return render(request,'ADMIN/verify doctor.html',{'dr':ob})


@login_required(login_url='/')
def admin_searchUser(request):
    name = request.POST['textfield']
    phone = request.POST['textfield']
    ob = user_reg_table.objects.filter(Q(name__icontains= name) |Q(phone__icontains=  phone))
    return render(request,'ADMIN/admin verify user.html',{'ur':ob})


@login_required(login_url='/')
def admin_view_users(request):
    ur = user_reg_table.objects.all()
    return render(request,'ADMIN/admin verify user.html',{'ur':ur})


@login_required(login_url='/')
def admin_acceptUser(request,lid):
    ob = login_table.objects.get(id = lid)
    ob.type = "user"
    ob.save()
    return HttpResponse('''<script> alert("Accepted!");window.location="/admin_view_users"</script>''')


@login_required(login_url='/')
def admin_rejectUser(request,lid):
    ob = login_table.objects.get(id=lid)
    ob.type = "Rejected"
    ob.save()
    return HttpResponse('''<script> alert("Rejected!"); window.location = "/admin_view_users"</script>''')


@login_required(login_url='/')
def admin_scheduleView(request):
    sc = schedule_table.objects.all()
    return render(request,'ADMIN/Tym schedule.html',{'sc':sc})

# def admin_doctorsBooking(request):
#     return render(request,'ADMIN/Bookings.html')


@login_required(login_url='/')
def admin_manageNotifictaion(request):
    he = notification_table.objects.all()
    return render(request,'ADMIN/Manage notification.html',{'he':he})


@login_required(login_url='/')
def admin_deleteNotification(request,id):
    ho = notification_table.objects.get(id = id)
    ho.delete()
    return HttpResponse('''<script> alert("Deleted!"); window.location = "/admin_manageNotifictaion"</script>''')



@login_required(login_url='/')
def admin_addNotificationpost(request):
    note = request.POST['textarea']
    date= request.POST['textfield2']
    oh = notification_table()
    oh.notification = note
    oh.date = date
    oh.save()
    return HttpResponse('''<script>alert("Posted Successfully");window.location = "/admin_manageNotifictaion"</script>"''')

# def admin_addNotification(request):
#     return render(request,)


@login_required(login_url='/')
def admin_addNotification(request):
    return render(request,'ADMIN/notification.html')


@login_required(login_url='/')
def admin_viewRatings(request):
    ov = user_rating_table.objects.all()
    return render(request,'ADMIN/doc ranking.html',{'ov':ov})


@login_required(login_url='/')
def admin_viewAllBooking(request,docid):
    request.session['docid'] = docid
    ob = booking_table.objects.filter(SCHEDULE__DOCTOR__id=docid)
    return render(request,'ADMIN/Ad viewBooking.html',{'ob':ob})



# @login_required(login_url='/')
# def admin_viewAllBooking1(request):
#     ob = booking_table.objects.filter(SCHEDULE__DOCTOR__id = request.session['docid'] )
# request.session['docid']=docid
# return redirect('/admin_viewAllBooking1')

@login_required(login_url='/')
def admin_searchDoctor1(request):
    name=request.POST['textfield']
    book = schedule_table.objects.filter(DOCTOR__name__icontains=name)
    data = []
    for i in book:
        ob = booking_table.objects.filter(SCHEDULE__id=i.id).count()
        # print(ob,"===================")
        row = {'name': i.DOCTOR.name, 'date': i.date, 'fromtime': i.fromtime, 'totime': i.totime, 'cnt': ob}
        data.append(row)
    return render(request, 'ADMIN/Bookings.html', {'book': data})


@login_required(login_url='/')
def admin_ViewBookings(request):
    book = schedule_table.objects.all()
    data = []
    for i in book:
        ob = booking_table.objects.filter(SCHEDULE__id=i.id).count()
        # print(ob,"===================")
        row = {'name': i.DOCTOR.name, 'date': i.date, 'fromtime': i.fromtime, 'totime': i.totime, 'cnt': ob,"docid":i.id}
        data.append(row)
    return render(request, 'ADMIN/Bookings.html', {'book': data})


@login_required(login_url='/')
def admin_viewRating(request):
    ob= user_rating_table.objects.all()
    return render(request,'ADMIN')


def admin_SearchScheduleByDate(request):
    date = request.POST['textfield']
    ob= schedule_table.objects.filter(date = date)
    return render(request,'ADMIN/Tym schedule.html',{'sc':ob} )

def admin_notiSearchDate(request):
    date = request.POST['textfield']
    ob = notification_table.objects.filter(date =date)
    return render(request,'ADMIN/Manage notification.html',{'he':ob})







#DOCTOR
@login_required(login_url='/')
def doctor_homePage(request):
    return render(request,'DOCTOR/doctor home.html')


@login_required(login_url='/')
def doctor_viewProfile(request):
    ob = doctor_reg_table.objects.get(LOGIN__id=request.session["lid"])
    return render(request,'DOCTOR/view profile.html',{"ob":ob})



@login_required(login_url='/')
def doctor_editDetails(request,id):
    request.session["did"] = id
    return redirect("doctor_editDetails1")


@login_required(login_url='/')
def doctor_editDetails1(request):
    ob = doctor_reg_table.objects.get(id= request.session["did"] )
    return render(request, 'DOCTOR/Edit details.html',{"ob":ob})


@login_required(login_url='/')
def doctor_editDetailsCode(request):
    name = request.POST['textfield']
    Designation = request.POST['textfield2']
    experience= request.POST['textfield3']
    place= request.POST['textfield4']
    pin= request.POST['textfield5']
    post= request.POST['textfield6']
    phone= request.POST['textfield7']

    if 'file' in request.FILES:
        image = request.FILES['file']
        fs = FileSystemStorage()
        fsave = fs.save(image.name, image)

        obj1 = doctor_reg_table.objects.get(id=request.session["did"])
        obj1.name = name
        obj1.image = fsave
        obj1.Designation = Designation
        obj1.experience = experience
        obj1.place = place
        obj1.pin = pin
        obj1.post = post
        obj1.phone = phone
        obj1.save()
    else:
        obj1 = doctor_reg_table.objects.get(id=request.session["did"])
        obj1.name = name
        obj1.Designation = Designation
        obj1.experience = experience
        obj1.place = place
        obj1.pin = pin
        obj1.post = post
        obj1.phone = phone
        obj1.save()


    return HttpResponse('''<script>alert ("edited Successfully!!"); window.location = "/doctor_viewProfile"</script>''')



@login_required(login_url='/')
def doctor_manageSchedules(request):

    ob = schedule_table.objects.filter(DOCTOR__LOGIN__id=request.session["lid"])
    return render(request,'DOCTOR/manage schedule.html',{'ob':ob})


@login_required(login_url='/')
def doctor_scheduleSearch(request):
    date = request.POST['textfield']
    search = schedule_table.objects.filter(date=date)
    return render(request,'DOCTOR/manage schedule.html',{'ob':search})


@login_required(login_url='/')
def doctor_viewNotifications(request):
    hh = notification_table.objects.all()
    return render(request,'DOCTOR/View notification.html',{'hh':hh})

def doctor_notiSearchByDate(request):
    aa = request.POST['textfield']
    ob = notification_table.objects.filter(date=aa)
    return render(request,'DOCTOR/View notification.html',{'hh':ob})



@login_required(login_url='/')
def doctor_addNewSchedule(request):
    return render(request,'DOCTOR/Schedule Adding.html')


@login_required(login_url='/')
def doctor_addNewScheduleCode(request):
    date = request.POST['textfield']
    timefrom = request.POST['textfield2']
    timeto = request.POST['textfield3']
    hh=doctor_reg_table.objects.get(LOGIN__id=request.session["lid"])
    schedule = schedule_table()
    schedule.DOCTOR_id=hh.id
    schedule.date = date
    schedule.fromtime = timefrom
    schedule.totime = timeto
    schedule.save()

    return HttpResponse('''<script>alert("Added Successfully");window.location="/doctor_manageSchedules"</script>''')



@login_required(login_url='/')
def doctor_viewBooking(request):
    ob = booking_table.objects.filter(SCHEDULE__DOCTOR__LOGIN__id= request.session['lid'])
    return render(request,'DOCTOR/view Booking.html',{'ob':ob})


@login_required(login_url='/')
def doctor_searchByDate(request):
    date1= request.POST['textfield']
    date2= request.POST['textfield2']
    ab = booking_table.objects.filter(SCHEDULE__date__gte = date1,SCHEDULE__date__lte = date2)
    print(ab,"==========================")
    return render(request, 'DOCTOR/view Booking.html', {'ob': ab,'dt1':date1,'dt2':date2})


@login_required(login_url='/')
def doctor_viewRating(request):
    ob = user_rating_table.objects.filter(DOCTOR__LOGIN__id = request.session['lid'])
    return render(request,'DOCTOR/View Ratig.html',{'ob':ob})


@login_required(login_url='/')
def doctor_changePassword(request):
    return render(request,'DOCTOR/Doctor Change password.html')


@login_required(login_url='/')
def doctor_changePasswordCode(request):
    current = request.POST['textfield']
    new = request.POST['textfield2']
    confirm = request.POST['textfield3']
    ob = login_table.objects.get(id=request.session["lid"])
    if ob.password == current:
        if new == confirm:
            ob.password = new
            ob.save()
            return HttpResponse('''<script>alert("changed Successfully!");window.location="/doctor_homePage"</script>''')
        else:
            return HttpResponse('''<script>alert("Password doesn't match!");window.location="/doctor_changePassword"</script>''')
    else:
        return HttpResponse(
            '''<script>alert("Current password does not match!");window.location="/doctor_changePassword"</script>''')


@login_required(login_url='/')
def doctor_viewBookingDeatils(request,id):
    oc = booking_table.objects.filter(USER__id = id)

    return render(request,'DOCTOR/patient details.html',{'oc':oc})


@login_required(login_url='/')
def doctor_viewLastFindings(request,id):
    ac = prescription_table.objects.filter(BOOKING__USER__id =id )
    return render(request,'DOCTOR/View last findings.html',{'ac':ac})



@login_required(login_url='/')
def doctor_uploadPrescriptionCode(request):
    image = request.FILES['file']
    findings = request.POST['textarea']

    fs = FileSystemStorage()
    fsave = fs.save(image.name, image)
    # print(request.session['lid'],"jjjjjjjjjjjjjjjjjj")
    ob = prescription_table()
    ob.LOGIN= login_table.objects.get(id = request.session['lid'])
    ob.BOOKING = booking_table.objects.get(id=request.session['bid'])
    ob.image = fsave
    ob.notes =findings
    ob.save()
    return HttpResponse('''<script> alert("Uploaded Successfully!!");window.location="/doctor_viewBooking"</script>''')


@login_required(login_url='/')
def doctor_uploadPrescription(request,id):
    request.session['bid']=id
    return render(request,'DOCTOR/prescription upload.html')

def doc_deleteSchedules(request,id):
    ob= schedule_table.objects.get(id=id)
    ob.delete()
    return HttpResponse('''<script> alert("Deleted");window.location="/doctor_manageSchedules"</script>''')













#USER

@login_required(login_url='/')
def user_homePage(request):
    return render(request,'USER/user home.html')

@login_required(login_url='/')
def user_view(request):
    return render(request,'USER/user home.html')

@login_required(login_url='/')
def user_changePasswordCode(request):
    current = request.POST['textfield']
    new = request.POST['textfield2']
    confirm = request.POST['textfield3']
    ob = login_table.objects.get(id=request.session["lid"])
    if ob.password == current:
        if new == confirm:
            ob.password = new
            ob.save()
            return HttpResponse('''<script>alert("changed Successfully!");window.location="/user_homePage"</script>''')
        else:
            return HttpResponse('''<script>alert("Password doesn't match!");window.location="/user_changePassword"</script>''')
    else:
        return HttpResponse(
            '''<script>alert("Current password does not match!");window.location="/user_changePassword"</script>''')


@login_required(login_url='/')
def user_changePassword(request):
    return render(request,'USER/user Change password.html')


@login_required(login_url='/')
def user_viewProfile(request):
    hh = user_reg_table.objects.get(LOGIN__id=request.session["lid"])
    return render(request,'USER/user view profile.html',{"hh":hh})


@login_required(login_url='/')
def user_editDetails(request,id):
    request.session["uid"] = id
    return redirect("user_editDetails1")


@login_required(login_url='/')
def user_editDetails1(request):
    hh = user_reg_table.objects.get(id= request.session["uid"])
    return render(request, 'USER/user Edit details.html',{"hh":hh})


@login_required(login_url='/')
def user_editDetailsCode(request):
    name = request.POST['textfield']
    email = request.POST['textfield2']
    place= request.POST['textfield4']
    pin= request.POST['textfield5']
    post= request.POST['textfield6']
    phone = request.POST['textfield7']

    if 'file' in request.FILES:
        image = request.FILES['file']
        fs = FileSystemStorage()
        fsave = fs.save(image.name, image)

        obj1 = user_reg_table.objects.get(id=request.session["uid"])
        obj1.name = name
        obj1.image = fsave
        obj1.place = place
        obj1.email = email
        obj1.pin = pin
        obj1.post = post
        obj1.phone = phone
        obj1.save()
    else:
        obj1 = user_reg_table.objects.get(id=request.session["uid"])
        obj1.name = name
        obj1.place = place
        obj1.email = email
        obj1.pin = pin
        obj1.post = post
        obj1.phone = phone
        obj1.save()


    return HttpResponse('''<script>alert ("edited Successfully!!"); window.location = "/user_viewProfile"</script>''')
#check

@login_required(login_url='/')
def user_viewDoctor(request):
    ai = doctor_reg_table.objects.filter(LOGIN__type='doctor')
    return render(request,'USER/view Doctors.html',{'ai':ai})


@login_required(login_url='/')
def user_searchDoctor(request):
    name = request.POST['textfield']
    ia = doctor_reg_table.objects.filter(name__icontains=name)
    return render(request, 'USER/view Doctors.html', {'ai': ia})



# def user_bookDoctor(request):
#     book = schedule_table.objects.all()
#     data=[]
#     for i in book:
#         ob=booking_table.objects.filter(SCHEDULE__id=i.id).count()
#         # print(ob,"===================")
#         row={'name':i.DOCTOR.name,'date':i.date,'fromtime':i.fromtime,'totime':i.totime,'cnt':ob}
#         data.append(row)
#     return render(request,'USER/View Schedules and book.html',{'book':data})


@login_required(login_url='/')
def user_viewAndRemoveBooking(request):
    ov= booking_table.objects.filter(USER__LOGIN__id=request.session['lid'])
    return render(request,'USER/View booking and remove.html',{'ov':ov})


@login_required(login_url='/')
def user_viewPrescription(request):
    ov=  prescription_table.objects.filter(BOOKING__USER__LOGIN=request.session['lid'])
    return render(request,'USER/view prescription.html',{'ov':ov})


@login_required(login_url='/')
def user_addRating(request):
    oj= doctor_reg_table.objects.filter(LOGIN__type = 'doctor')
    return render(request,'USER/Send Rating.html',{'oj':oj})


@login_required(login_url='/')
def user_sendRating(request):
    # print(request.session['lid'],"bbbbbbbbbbbbbbbbbbbb")
    ob1=user_reg_table.objects.get(LOGIN__id=request.session['lid'])

    oc = request.POST['rating']
    co = request.POST['doc']
    ob=user_rating_table()
    ob.DOCTOR = doctor_reg_table.objects.get(id = co)
    ob.rating =oc
    ob.date = datetime.datetime.today()
    ob.USER = user_reg_table.objects.get(id=ob1.id)
    ob.save()
    return HttpResponse('''<script> alert("Rating send");window.location="/user_addRating"</script>''')


# def admin_bookDoctor(request):
#     book = schedule_table.objects.all()
#     data=[]
#     for i in book:
#         ob=booking_table.objects.filter(SCHEDULE__id=i.id).count()
#         # print(ob,"===================")
#         row={'name':i.DOCTOR.name,'date':i.date,'fromtime':i.fromtime,'totime':i.totime,'cnt':ob}
#         data.append(row)
#     return render(request,'ADMIN/Bookings.html',{'book':data})






@login_required(login_url='/')
def user_bookDoctor(request,id):
    ob= schedule_table.objects.filter(DOCTOR__id =id )
    return render(request,'USER/View Schedules and book.html',{'ob':ob})


@login_required(login_url='/')
def user_bookDoctor1(request,id):
    ob= schedule_table.objects.filter(DOCTOR__id =id )
    return render(request,'USER/View Schedules and book.html',{'ob':ob})


@login_required(login_url='/')
def user_booking(request,id):
    gg = user_reg_table.objects.get(LOGIN__id=request.session['lid'])
    ok=booking_table.objects.filter(USER=gg.id,SCHEDULE=id)
    if len(ok)==0:
        ob =  booking_table()
        ob.date = datetime.datetime.today()
        ob.time = datetime.datetime.now()
        ob.SCHEDULE=schedule_table.objects.get(id=id)
        ob.USER=user_reg_table.objects.get(id=gg.id)
        ob.save()
        return HttpResponse(''' <script>alert("BOOKED Successfully!!");window.location="/user_viewDoctor"</script>''')
    else:
        return HttpResponse(''' <script>alert("Already BOOKED!!");window.location="/user_viewDoctor"</script>''')


@login_required(login_url='/')
def user_searchDoctor2(request):
    name=request.POST['textfield']
    bo = schedule_table.objects.filter(DOCTOR__name__istartswith=name )
    return render(request,'USER/View Schedules and book.html',{'ob':bo})

@login_required(login_url='/')
def user_deleteSchedule(request,id):
    oh= booking_table.objects.get(id=id)
    oh.delete()
    return HttpResponse(''' <script>alert("Deleted!!");window.location="/user_viewAndRemoveBooking"</script>''')


@login_required(login_url='/')
def logout(request):
    auth.logout(request)
    return render(request,'Login.html')


#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


def flut_login(request):
    print(request.POST)
    username= request.POST['username']
    password = request.POST['password']
    try:
        ob = login_table.objects.get(username=username, password = password,type = 'user')
        # print(ob,"hhhhhhhhhhhhhhhhhhhhhh")
        return JsonResponse({"status": "ok", "lid": ob.id})
    except:
        # print("hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh")
        return JsonResponse({"task": "ok"})



def flut_register(request):
    try:
        name = request.POST['name']
        image = request.POST['image']
        email = request.POST['email']
        phone = request.POST['phone']
        place = request.POST['place']
        post =request.POST['post']
        pin = request.POST['pin']
        uname = request.POST['uname']
        pswrd = request.POST['pswrd']

        import base64
        timestr = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        print(timestr)
        a=base64.b64decode(image)
        fh =open(r"C:\Users\ASUS\PycharmProjects\DrBooking\media\flut_image\\" + timestr +".jpg","wb")
        path="/flut_image/"+timestr+".jpg"
        fh.write(a)
        fh.close()

        ob1 = login_table()
        ob1.username =uname
        ob1.password = pswrd
        ob1.type = "pending"
        ob1.save()


        ob =user_reg_table()
        ob.LOGIN = ob1
        ob.name= name
        ob.email = email
        ob.phone = phone
        ob.place= place
        ob.post = post
        ob.pin= pin
        ob.image =path
        ob.save()
        return JsonResponse({"task":"ok"})
    except Exception as e:
        print(e)
        return JsonResponse({"task":"Invalid"})





def flut_userProfile(request):
    lid=request.POST['lid']
    i = user_reg_table.objects.get(LOGIN_id=lid)
    return JsonResponse({
            'status': 'ok','name': i.name,
        'image': i.image.url,
        'email': i.email,
        'phone': str(i.phone),
        'place': i.place,
        'post': i.post,
        'pin': i.pin,

        })


def flut_viewDoctors(request):
    a = doctor_reg_table.objects.filter(LOGIN__type='doctor')
    l=[]
    for i in a:
        l.append({'id':i.id,'name':i.name,'image':i.image.url,'Designation':i.Designation})
    print(l)


    return JsonResponse({
        'status': 'ok' ,
        'data':l
    })

def flut_bookDoctor(request):
    id=request.POST['did']
    f = schedule_table.objects.filter(DOCTOR__id=id )
    b=[]
    for i in f:
        b.append({



        'id':id,
        'name':i.DOCTOR.name,
        'date': str(i.date),
        'fromtime':i.fromtime,
        'totime':i.totime,
        'image':str(i.DOCTOR.image.url),

    })
    print(b)

    return JsonResponse({
        'status': 'ok',
        'data':b
    })

# def flut_bookingDoctor(request):
#     iv= request.POST['lid']
#     ic = request.POST['sid']
#
#
#     ob = booking_table()
#     ob.date= datetime.datetime.today().date()
#     ob.time = datetime.datetime.now().today().time()
#     ob.SCHEDULE  = schedule_table.objects.get(id=ic)
#     ob.USER = user_reg_table.objects.get(LOGIN_id=iv)
#     ob.save()
#     return JsonResponse({"status": "ok"})



import datetime
from django.http import JsonResponse
from .models import booking_table, schedule_table, user_reg_table

def flut_bookingDoctor(request):
    iv = request.POST['lid']
    ic = request.POST['sid']

    existing_booking = booking_table.objects.filter(SCHEDULE_id=ic, USER__LOGIN_id=iv).exists()

    if existing_booking:
        return JsonResponse({"status": "not ok ", "message": "Schedule already booked"})

    ob = booking_table()
    ob.date = datetime.datetime.today().date()
    ob.time = datetime.datetime.now().time()
    ob.SCHEDULE = schedule_table.objects.get(id=ic)
    ob.USER = user_reg_table.objects.get(LOGIN_id=iv)
    ob.save()

    return JsonResponse({"status": "ok"})




def flut_viewBooking(request):
    a = request.POST['lid']
    o = booking_table.objects.filter(USER__LOGIN_id = a)
    c = []
    for i in o:
        c.append({
            'id':i.id,
            'name':i.SCHEDULE.DOCTOR.name,
            'date':i.date,
            'time': i.time,



        })
    # print(c)
    return JsonResponse({
        'status':'ok',
        'data':c

    })


def flut_deleteBooking(request):
    id = request.POST['id']
    a = booking_table.objects.get(id=id)
    a.delete()
    return JsonResponse({'status':"ok"})


def flut_viewPrescription(request):
    id = request.POST['lid']
    b = prescription_table.objects.filter(BOOKING__USER__LOGIN_id=id)
    c=[]
    for i in b:
        c.append({
            'id':i.id,
            'name':i.BOOKING.SCHEDULE.DOCTOR.name,
            'image':i.image.url,
            'date':i.BOOKING.SCHEDULE.date,
            'fromtime':i.BOOKING.SCHEDULE.fromtime,
            'totime':i.BOOKING.SCHEDULE.totime,
            'notes':i.notes
        })
        print(c)
    return JsonResponse({
        'status': 'ok',
        'data': c

    })

def flut_sendRating(request):
    b= request.POST['rating']
    id= request.POST['lid']
    did= request.POST['did']
    # c = user_reg_table.objects.get(LOGIN__id = id)
    # d = doctor_reg_table.objects.filter(LOGIN__type = 'doctor')


    ob=user_rating_table()
    ob.DOCTOR= doctor_reg_table.objects.get(id = did)
    ob.rating =b
    ob.USER =   user_reg_table.objects.get(LOGIN__id = id)
    ob.date = datetime.datetime.today().date()
    ob.save()

    return JsonResponse({
        'status':'ok'
    })

def flut_changePassword(request):
    old = request.POST['old']
    newpass = request.POST['a']
    confirm = request.POST['confirm']
    lid = request.POST['lid']

    a=login_table.objects.filter(id=lid,password=old)
    if a.exists():
        if newpass==confirm:
            a1 = login_table.objects.filter(id=lid, password=old).update(password=confirm)
            return JsonResponse({'status': 'ok'})
        else:
            return JsonResponse({'status': 'not ok'})
    else:
        return JsonResponse({'status': 'not ok'})



def flut_detailedPrescription(request):
    id = request.POST['lid']
    b = prescription_table.objects.filter(BOOKING__USER__LOGIN_id=id)
    c=[]
    for i in b:
        c.append({
            'id':i.id,
            'name':i.BOOKING.SCHEDULE.DOCTOR.name,
            'image':i.image.url,
            'date':i.BOOKING.SCHEDULE.date,
            'fromtime':i.BOOKING.SCHEDULE.fromtime,
            'totime':i.BOOKING.SCHEDULE.totime,
            'notes':i.notes
        })
        print(c)
    return JsonResponse({
        'status': 'ok',
        'data': c

    })

def flut_searchDoctors(request):
    name= request.POST['name']
    a= doctor_reg_table.objects.filter(name__icontains = name)
    c=[]
    for i in a:
        c.append({
            'id': i.id,
            'name':i.name,
            'image':i.image.url,

        })
    return JsonResponse({
        'status':'ok',
        'data': c
    })












# def user_searchDoctor(request):
#     name = request.POST['textfield']
#     ia = doctor_reg_table.objects.filter(name__icontains=name)
#     return render(request, 'USER/view Doctors.html', {'ai': ia})


