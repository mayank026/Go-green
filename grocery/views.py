from email import message
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,logout,login
from .models import *
from datetime import date
from .helpers import *
import json
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt

from .models import *
from datetime import date
import razorpay


razorpay_id = "rzp_test_eLHZz9ToSi7WdG"
razorpay_secret_key= "iqUuVsFMnZSrUayDG3KazepZ"
client = razorpay.Client(auth=(razorpay_id,razorpay_secret_key))

# Create your views here.

def Home(request):
    cat = ""
    pro = ""
    cat = ""
    num = 0
    num1 = 0
    cat = Category.objects.all()
    pro = Product.objects.all()
    num = []
    num1 = 0
    try:
        user = User.objects.get(id=request.user.id)
        profile = Profile.objects.get(user=user)
        cart = Cart.objects.filter(profile=profile)
        for i in cart:
            num1 += 1

    except:
        pass
    a = 1
    li = []

    for j in pro:
        b = 1
        for i in cat:
            if i.name == j.category.name:
                if not j.category.name in li:
                    li.append(j.category.name)
                    if b == 1:
                        num.append(a)
                        b = 2
        a += 1


    d = {'pro': pro, 'cat': cat,'num':num,'num1':num1}
    return render(request, 'all_product.html', d)
	

def About(request):
    return render(request, 'about.html')
	

def Contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        error_msg = ""
        if not name:
            error_msg = "Enter your name !"
        if not email:
            error_msg = "Enter your email !"
        if not phone:
            error_msg = "Enter your phone !"
        if not message:
            error_msg = "Enter your message !"
        if not error_msg:
            # contact = Contact(name=name, email=email,
            #                   phone=phone, message=message)
            # contact.save()
            context = {"name": name, "email": email,
                       "phone": phone, "message": message}
            mail_to_admin(context)
            messages.info(
                request, "Your message was sent, We'll contact you soon, Thank you!")
        else:
            context = {'error_condition': error_msg}
            return render(request, "contact.html", context)
    return render(request, "contact.html")


def Signup(request):
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        u = request.POST['uname']
        p = request.POST['pwd']
        d = request.POST['date']
        c = request.POST['city']
        ad = request.POST['add']
        e = request.POST['email']
        i = request.FILES['img']
        con = request.POST['contact']
        error_msg = ""
        
        check = User.objects.filter(email=e).exists()
        if check:
            print('email registerd')
            error_msg = "email already registered"
            context = {"error_condition": error_msg}
            return render(request, "signup.html", context)
        elif User.objects.filter(username=u).exists():
            
            error_msg = "username has already taken"
            context = {"username_error": error_msg}
            return render(request, "signup.html", context)
        else:
            user = User.objects.create_user(username=u, email=e, password=p, first_name=f,last_name=l)
            user.save()
            auth_token = str(uuid.uuid4())
            Profile.objects.create(user=user, dob=d, city=c, address=ad, contact=con,image=i,verified=auth_token)

            send_mail_after_registration(e, auth_token)
            context = {"mail_sent": 'Activation link has sent to your mail'}
            return render(request, "signup.html", context)

    return render(request, "signup.html")


def VerifyAccount(request,token):
    try:
        profile_obj = Profile.objects.filter(verified=token).first()

        if profile_obj:
            print('success')
            profile_obj.verified = "True"
            profile_obj.save()
            context = {
                "verify_message": 'Your account verified successfully.'}
            return render(request, "token.html", context)
        else:
            return redirect('/error')
    except Exception as e:
        print(e)
        return redirect('/')
    
def error(request):
    return render(request, "error.html")


def Login(request):
    error = ""
    if request.method == "POST":
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        try:
            if user:
                login(request, user)
                error = "yes"
            else:
                error = "not"
        except:
            error="not"
    d = {'error': error}
    return render(request,'login.html',d)


def Admin_Login(request):
    error = ""
    if request.method == "POST":
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        try:
            if user.is_staff:
                login(request, user)
                error = "yes"
            else:
                error = "not"
        except:
            error="not"
    d = {'error': error}
    return render(request,'loginadmin.html',d)


def Logout(request):
    logout(request)
    return redirect('home')


def View_user(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    pro = Profile.objects.all()
    d = {'user':pro}
    return render(request,'view_user.html',d)



def Add_Product(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    cat = Category.objects.all()
    error=False
    if request.method=="POST":
        c = request.POST['cat']
        p = request.POST['pname']
        pr = request.POST['price']
        i = request.FILES['img']
        d = request.POST['desc']
        ct = Category.objects.get(name=c)
        Product.objects.create(category=ct, name=p, price=pr, image=i, desc=d)
        error=True
    d = {'cat': cat,'error':error}
    return render(request, 'add_product.html', d)


def All_product(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user = User.objects.get(id=request.user.id)
    profile = Profile.objects.get(user=user)
    cart = Cart.objects.filter(profile=profile)
    num1=0
    for i in cart:
        num1 += 1
    cat = Category.objects.all()
    pro = Product.objects.all()
    d ={'pro':pro,'cat':cat,'num1':num1}
    return render(request,'all_product.html',d)


def Admin_View_Booking(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    book = Booking.objects.all()
    d = {'book': book}
    return render(request, 'admin_viewBokking.html', d)


def View_feedback(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    feed = Send_Feedback.objects.all()
    d = {'feed': feed}
    return render(request, 'view_feedback.html', d)


def View_prodcut(request,pid):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    cat = ""
    cat1 = ""
    pro1 = ""
    num1 = 0
    user=""
    profile=""
    cart=""
    pro=""
    num=""
    if not request.user.is_staff:
        user = User.objects.get(id=request.user.id)
        profile = Profile.objects.get(user=user)
        cart = Cart.objects.filter(profile=profile)
        for i in cart:
            num1 += 1

    if pid == 0:
        cat = "All Product"
        pro1 = Product.objects.all()
    else:
        cat1 = Category.objects.get(id=pid)
        pro1 = Product.objects.filter(category=cat1).all()
    cat = Category.objects.all()
    pro = Product.objects.all()
    num = []
    b = 1
    for j in cat:
        a = 1
        for i in pro:
            if j.name == i.category.name:
                if a == 1:
                    num.append(i.id)
                    a = 2
    d = {'pro': pro, 'cat': cat,'cat1': cat1,'num':num,'pro1':pro1,'num1':num1}
    return render(request, 'view_product.html',d)


def Add_Categary(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    error=False
    if request.method=="POST":
        n = request.POST['cat']
        Category.objects.create(name=n)
        error=True
    d = {'error':error}
    return render(request, 'add_category.html', d)


def View_Categary(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    pro = Category.objects.all()
    d = {'pro': pro}
    return render(request,'view_category.html', d)



def View_Booking(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user = User.objects.get(id=request.user.id)
    profile = Profile.objects.get(user=user)
    cart = Cart.objects.filter(profile=profile)
    book = Booking.objects.filter(profile=profile).select_related()
    num1=0
    for i in cart:
        num1 += 1
    d = {'book': book,'num1':num1}
    return render(request, 'view_booking.html', d)


def Feedback(request, pid):
    if not request.user.is_authenticated:
        return redirect('login')
    error = False
    user1 = User.objects.get(id=request.user.id)
    profile = Profile.objects.get(user=user1)
    cart = Cart.objects.filter(profile=profile)
    num1 =0
    for i in cart:
        num1 += 1
    date1 = date.today()
    user = User.objects.get(id=pid)
    pro = Profile.objects.filter(user=user).first()
    if request.method == "POST":
        d = request.POST['date']
        u = request.POST['uname']
        e = request.POST['email']
        con = request.POST['contact']
        m = request.POST['desc']
        user = User.objects.filter(username=u, email=e).first()
        pro = Profile.objects.filter(user=user, contact=con).first()
        Send_Feedback.objects.create(profile=pro, date=d, message1=m)
        error = True
    d = {'pro': pro, 'date1': date1,'num1':num1,'error':error}
    return render(request, 'feedback.html', d)

def Change_Password(request):
    if not request.user.is_authenticated:
        return redirect('login')
    msg=""
    num1=0
    user = User.objects.get(id=request.user.id)
    profile = Profile.objects.get(user=user)
    cart = Cart.objects.filter(profile=profile)
    for i in cart:
        num1 += 1
    if request.method=="POST":
        n = request.POST['pwd1']
        c = request.POST['pwd2']
        
        if c == n:
            u = User.objects.get(username__exact=request.user.username)
            u.set_password(n)
            u.save()
            msg="Password successfully changed"
        else:
            msg = "Error occured"
    d = {'error':msg,'num1':num1}
    return render(request,'change-password.html',d)



def Add_Cart(request,pid):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method=="POST":
        user = User.objects.get(id=request.user.id)
        profile = Profile.objects.get(user=user)
        product = Product.objects.get(id=pid)
        check  = Cart.objects.filter(Q(profile=profile) & Q(product=product)).exists()
        if not check :
            Cart.objects.create(profile=profile, product=product)
        return redirect('cart')

def view_cart(request):
    if not request.user.is_authenticated:
        return redirect('login')
    getpid = request.GET.get('pid', 0)
    getmid = request.GET.get('mid', 0)
    # getcart = request.GET.get('cart', 0)
    limit=0
    if getpid:
        mydata = Cart.objects.get(id=getpid)
        if int(mydata.quantity) :
            mydata.quantity = int(mydata.quantity) + 1

            if(mydata.quantity >= mydata.product.qty):
                mydata.quantity=mydata.product.qty
                limit=1
            elif(mydata.quantity >5):
                mydata.quantity=5

            mydata.total = (int(mydata.quantity))*int(mydata.product.price)
            mydata.save()
    if getmid:
        mydata = Cart.objects.get(id=getmid)
        if int(mydata.quantity) > 1:
            mydata.quantity = int(mydata.quantity) - 1
            mydata.total = (int(mydata.quantity))*int(mydata.product.price)
            mydata.save()

    user = User.objects.get(id=request.user.id)
    profile = Profile.objects.get(user=user)
    cart =  Cart.objects.filter(profile=profile).all()
    total=0
    num1=0
    book_id=request.user.username
    message1="Here ! No Any Product"
    for i in cart:
        total+=i.product.price
        num1+=1
        book_id = book_id+"."+str(i.product.id)
    d = {'profile':profile,'cart':cart,'total':total,'num1':num1,'book':book_id,'message':message1,'limit':limit}
    return render(request,'cart.html',d)



def remove_cart(request,pid):
    if not request.user.is_authenticated:
        return redirect('login')
    cart = Cart.objects.get(id=pid)
    cart.delete()
    return redirect('cart')

def Booking_order(request, pid):
    if not request.user.is_authenticated:
        return redirect('login')
    data1 = User.objects.get(id=request.user.id)
    data = Profile.objects.filter(user=data1).first()
    cart = Cart.objects.filter(profile=data).all()
    
    total = 0
    num1=0
    for i in cart:
        total+=(int (i.product.price)*int (i.quantity))
    user1 = data1.username
    li = pid.split('.')
    li2 = []
    for j in li:
        if user1 != j:
            li2.append(int(j))
            num1+=1
    date1 = date.today()
    if request.method == "POST":
        d = request.POST['date1']
        c = request.POST['name']
        c1 = request.POST['city']
        ad = request.POST['add']
        e = request.POST['email']
        con = request.POST['contact']
        b = request.POST['book_id']
        t = request.POST['total']
        user = User.objects.get(username=c)
        profile = Profile.objects.get(user=user)
        status = Status.objects.get(name="pending")
       
        notes = {'order-type': "basic order from the website", 'key':'value'}
        razorpay_order = client.order.create({'amount':int(total)*100, 'currency':'INR', 'notes' : notes,  'payment_capture':'1'})
        print("razorpay=")
        book1 = Booking.objects.create(provider_order_id=razorpay_order['id'],profile=profile, book_date=d,booking_id=b,total=t,quantity=num1,status=status)
        cart2 = Cart.objects.filter(profile=profile).all()
        cart2.delete()
        razorpay_order_id=razorpay_order['id']
        return redirect('payment',book1.total,razorpay_order_id)
    d = {'data': data, 'data1': data1, 'book_id': pid, 'date1': date1,'total':total,'num1':num1}
    return render(request, 'booking.html', d)


def payment(request,total,razorpay_order_id):
    if request.method == "GET":
        print("madhuri")
        
        
    if request.method == "POST":
        print( razorpay_order_id)
    return render(
            request,
            "payment.html",
            {
                "callback_url": "http://" + "127.0.0.1:8000" + "/callback/",
                "razorpay_key": razorpay_id,
                'razorpay_order' :Booking, 
                 "order_id":razorpay_order_id,
                
                
            },
            )
    return render(request,'payment.html',{'total':int(total)*100,'api_key':razorpay_id})

   
               
@csrf_exempt
def callback(request):
    def verify_signature(response_data):
        client = razorpay.Client(auth=(razorpay_id,razorpay_secret_key))
        return client.utility.verify_payment_signature(response_data)

    if "razorpay_signature" in request.POST:
        payment_id = request.POST.get("razorpay_payment_id", "")
        provider_order_id = request.POST.get("razorpay_order_id", "")
        signature_id = request.POST.get("razorpay_signature", "")
        
        print(provider_order_id)

        order = Booking.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.signature_id = signature_id
        order.save()
        if  verify_signature(request.POST):
            order.status = PaymentStatus.SUCCESS
            order.save()
            return render(request, "paymentsuccess.html", context={"status": order.status})
        else:
            order.status = PaymentStatus.FAILURE
            order.save()
            return render(request, "paymentfailed.html", context={"status": order.status})
    else:
        payment_id = json.loads(request.POST.get("error[metadata]")).get("payment_id")
        provider_order_id = json.loads(request.POST.get("error[metadata]")).get(
            "order_id"
        )
        order = Booking.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.status = PaymentStatus.FAILURE
        order.save()
        return render(request, "paymentfailed.html", context={"status": order.status})
        
def delete_admin_booking(request, pid,bid):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    book = Booking.objects.get(booking_id=pid,id=bid)
    book.delete()
    return redirect('admin_viewBooking')

def delete_booking(request, pid,bid):
    if not request.user.is_authenticated:
        return redirect('login')
    book = Booking.objects.get(booking_id=pid,id=bid)
    book.delete()
    return redirect('view_booking')

def delete_user(request, pid):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    user = User.objects.get(id=pid)
    user.delete()
    return redirect('view_user')

def delete_feedback(request, pid):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    feed = Send_Feedback.objects.get(id=pid)
    feed.delete()
    return redirect('view_feedback')


def booking_detail(request,pid,bid):
    if not request.user.is_authenticated:
        return redirect('login')
    user = User.objects.get(id=request.user.id)
    profile = Profile.objects.get(user=user)
    cart =  Cart.objects.filter(profile=profile).all()
    product = Product.objects.all()
    book = Booking.objects.get(booking_id=pid, id=bid)
    total=0
    num1=0
    user1 = user.username
    li = book.booking_id.split('.')
    li2=[]
    for j in li:
        if user1!= j :
            li2.append(int(j))
    for i in cart:
        total+=i.product.price
        num1+=1
    d = {'profile':profile,'cart':cart,'total':total,'num1':num1,'book':li2,'product':product,'total':book}
    return render(request,'booking_detail.html',d)


def admin_booking_detail(request,pid,bid,uid):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    user = User.objects.get(id=uid)
    profile = Profile.objects.get(user=user)
    cart =  Cart.objects.filter(profile=profile).all()
    product = Product.objects.all()
    book = Booking.objects.get(booking_id=pid, id=bid)
    total=0
    num1=0
    user1 = user.username
    li = book.booking_id.split('.')
    li2=[]
    for j in li:
        if user1!= j :
            li2.append(int(j))
    for i in cart:
        total+=i.product.price
        num1+=1
    d = {'profile':profile,'cart':cart,'total':total,'num1':num1,'book':li2,'product':product,'total':book}
    return render(request,'admin_view_booking_detail.html',d)

def Edit_status(request,pid,bid):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    book = Booking.objects.get(booking_id=pid,id=bid)
    stat = Status.objects.all()
    if request.method == "POST":
        n = request.POST['book']
        s = request.POST['status']
        book.booking_id = n
        sta = Status.objects.filter(name=s).first()
        book.status = sta
        book.save()
        return redirect('admin_viewBooking')
    d = {'book': book, 'stat': stat}
    return render(request, 'status.html', d)


def Admin_View_product(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    pro = Product.objects.all()
    d = {'pro':pro}
    return render(request,'admin_view_product.html',d)

def delete_product(request,pid):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    pro = Product.objects.get(id=pid)
    pro.delete()
    return redirect('admin_view_product')

def profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user = User.objects.get(id=request.user.id)
    pro = Profile.objects.get(user=user)
    cart=[]
    
    # cart = Cart.objects.get(profile=pro)
    cart = Cart.objects.filter(profile=pro)
    
    num1 = 0
    total = 0
    for i in cart:
        total += i.product.price
        num1 += 1
    user = User.objects.get(id=request.user.id)
    pro = Profile.objects.get(user=user)
    d={'pro':pro,'user':user,'num1':num1,'total':total}
    return render(request,'profile.html',d)


def Edit_profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    error = False
    user=User.objects.get(id=request.user.id)
    pro = Profile.objects.get(user=user)
    cart = ""
    try:
        cart = Cart.objects.get(profile=pro)
    except:
        pass
    num1=0
    total=0
    for i in cart:
        total+=i.product.price
        num1+=1
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        u = request.POST['uname']
        c = request.POST['city']
        ad = request.POST['add']
        e = request.POST['email']
        con = request.POST['contact']
        d = request.POST['date']

        try:
            i = request.FILES['img']
            pro.image = i
            pro.save()

        except:
            pass


        if d:
            try:
                pro.dob = d
                pro.save()
            except:
                pass
        else:
            pass

        pro.user.username=u
        pro.user.first_name=f
        pro.user.last_name=l
        pro.user.email=e
        pro.contact=con
        pro.city=c
        pro.address=ad
        pro.save()
        error = True
    d = {'error':error,'pro':pro,'num1':num1,'total':total}
    return render(request, 'edit_profile.html',d)

def Admin_Home(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    book = Booking.objects.all()
    customer = Profile.objects.all()
    pro = Product.objects.all()
    total_book = 0
    total_customer = 0
    total_pro = 0
    for i in book:
        total_book+=1
    for i in customer:
        total_customer+=1
    for i in pro:
        total_pro+=1
    d = {'total_pro':total_pro,'total_customer':total_customer,'total_book':total_book}
    return render(request,'admin_home.html',d)

def delete_category(request,pid):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    cat = Category.objects.get(id=pid)
    cat.delete()
    return redirect('view_categary')

def edit_product(request,pid):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    cat = Category.objects.all()
    product = Product.objects.get(id=pid)
    error=""
    if request.method=="POST":
        c = request.POST['cat']
        p = request.POST['pname']
        pr = request.POST['price']
        d = request.POST['desc']
        ct = Category.objects.get(name=c)
        product.category = ct
        product.name = p
        product.price = pr
        product.desc = d
        try:
            product.save()
            error = "no"
        except:
            error = "yes"
        try:
            i = request.FILES['img']
            product.image = i
            product.save()
        except:
            pass  # pass is a null statement. no operation.

    d = {'cat': cat,'error':error,'product':product}
    return render(request, 'edit_product.html', d)


def edit_category(request,pid):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    category = Category.objects.get(id=pid)
    error=""
    if request.method=="POST":
        c = request.POST['cat']
        category.name = c
        try:
            category.save()
            error = "no"
        except:
            error = "yes"
    d = {'error':error,'category':category}
    return render(request, 'edit_category.html', d)


def add_blogpost(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    error = ""
    if request.method=="POST":
        pt = request.POST['posttitle']
        pd = request.POST['postdetail']
        pi = request.FILES['postimage']
        postd = date.today()
        try:
            Blogpost.objects.create(posttitle=pt,postdetail=pd,postimage=pi,postdate=postd)
            error = "no"
        except:
            error = "yes"
    d = {'error':error}
    return render(request, 'add_blogpost.html', d)


def view_blogpost(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    blogpost = Blogpost.objects.all()
    d = {'blogpost': blogpost}
    return render(request,'view_blogpost.html', d)

def delete_blogpost(request,pid):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    blogpost = Blogpost.objects.get(id=pid)
    blogpost.delete()
    return redirect('view_blogpost')


def edit_blogpost(request,pid):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    blogpost = Blogpost.objects.get(id=pid)
    error=""
    if request.method=="POST":
        pt = request.POST['posttitle']
        pd = request.POST['postdetail']


        try:
            blogpost.posttitle = pt
            blogpost.postdetail = pd
            blogpost.save()
            error = "no"
        except:
            error = "yes"
        try:
            pi = request.FILES['postimage']
            blogpost.postimage = pi
            blogpost.save()
        except:
            pass  # pass is a null statement. no operation.

    d = {'error':error,'blogpost':blogpost}
    return render(request, 'edit_blogpost.html', d)

def blogs(request):
    blogpost = Blogpost.objects.all()
    d = {'blogpost': blogpost}
    return render(request,'blogs.html',d)

def blogdetail(request,pid):
    blogpost = Blogpost.objects.get(id=pid)
    d = {'blogpost': blogpost}
    return render(request,'blogdetail.html',d)

import uuid

def ForgetPassword(request):
    try:
        if request.method == 'POST':
            email = request.POST.get('email')
            msg=""
            if not User.objects.filter(email=email).first():
                
                msg="Email not registered..."
                context={'message':msg}
                return render(request,"forget-password.html",context)
            
            user_obj = User.objects.get(email = email)
            token = str(uuid.uuid4())
            profile_obj= Profile.objects.get(user = user_obj)
            profile_obj.forget_password_token = token
            profile_obj.save()
            send_forget_password_mail(user_obj.email , token)
            msg="Reset link has sent to your mail"
            context = {'message':msg}
            return render(request,"forget-password.html",context)
    except Exception as e:
        print(e)
    return render(request , 'forget-password.html')

def ResetPassword(request , token):
    context = {}
    
    try:
        if token =='null':
            return render(request,'error.html')
        else:
            profile_obj = Profile.objects.filter(forget_password_token = token).first()
            if not profile_obj:
                return render(request,'error.html')
            context = {'user_id' : profile_obj.user.id}
        
        if request.method == 'POST':
            new_password = request.POST.get('pwd1')
            confirm_password = request.POST.get('pwd2')
            user_id = request.POST.get('user_id')
            
            if user_id is  None:
                messages.info(request, 'No user id found.')
                return redirect(f'/reset-password/{token}/')
                
            
            if  new_password != confirm_password:
                messages.add_message(request, messages.INFO, 
                'both password should be equal.', 
                    extra_tags='ex-tag')
                #messages.info(request, 'both password should  be equal.')
                return redirect(f'/reset-password/{token}/')
                         
            
            user_obj = User.objects.get(id = user_id)
            user_obj.set_password(new_password)
            user_obj.save()
            profile_obj.forget_password_token='null'
            profile_obj.save()
            context = {
                "verify_message": 'Your Password changed successfully.'}
            return render(request, "token.html", context)
            
    except Exception as e:
        print(e)
        
    return render(request , 'change-password.html' , context)
