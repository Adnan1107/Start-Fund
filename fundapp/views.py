from django.shortcuts import render,redirect,HttpResponse
from .models import registration,founderregisration,investorregistration, Investment, Payment,Paymen
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.core.mail import send_mail

# Create your views here.
def index(request):
    return render(request,'index.html')

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.core.mail import send_mail

@csrf_protect
def submit_contact(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            email = request.POST.get('email')
            message = request.POST.get('message')

            # Printing received data for debugging (you may remove this in production)
            print(f"Data Received: Name - {name}, Email - {email}, Message - {message}")

            # Construct the email message and send it to your business email, not the sender's
            send_mail(
                subject=f"New Contact from {name}",
                message=f"You have received a new message from your website contact form.\n\n"
                        f"Name: {name}\nEmail: {email}\nMessage: {message}",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.EMAIL_HOST_USER],  # Should be your business email
            )
            return HttpResponse(f"Thank you {name}, we have received your message!")
        except Exception as e:
            print(f"Error in processing the form: {e}")
            return HttpResponse(f"Error in sending email: {str(e)}")
    else:
        print("Not a POST request.")
    return render(request, 'contact.html')

def home(request):
    return render(request,'home.html')

def userhome(request):
    return render(request,'userhome.html')

def admin_dashboard(request):
    return render(request,'admin_dashboard.html')
def register(request):
    if request.method =='POST':
        username=request.POST.get('username')
        business=request.POST.get('businessname')
        email=request.POST.get('email')
        password=request.POST.get('password')
        phone=request.POST.get('phone')
        profilepic=request.FILES.get('image')  
        registration(username=username, business=business,email=email,password=password,profilepic=profilepic,phone=phone).save()
        return redirect('home')
    return render(request,'register.html')  


def login(request):
    if request.method =='POST':
        username=request.POST.get('username')
        print(username)
        password=request.POST.get('password')
        print(password)
        try:
            user=registration.objects.get(username=username,password=password)
            print("y",user)
            semail=user.email
            request.session['email']=semail
            return redirect('userhome')
        except Exception as e:
            print("h",e)
            msg="invalid password or email"
            return render(request,'login.html',{"msg":msg})
    return render(request,'login.html')

def profile(request):
    if 'email'in request.session:
        mail=request.session['email']
        usr=founderregisration.objects.get(email=mail)
        return render(request,'profile.html',{'usr':usr})
    return redirect('founderlogin')

def investorprofile(request):
    if 'email'in request.session:
        mail=request.session['email']
        usr=investorregistration.objects.get(email=mail)
        return render(request,'investorprofile.html',{'usr':usr})
    return redirect('/investor_login/')

def indelete(request):
    if 'email'in request.session:
        mail=request.session['email']
        usr=investorregistration.objects.get(email=mail)
        return render(request,'indelete.html',{'usr':usr})
    return redirect('/investor_login/')

def investordeleteconfirm(request):
    if 'email' in request.session:
        email=request.session['email']
        us=investorregistration.objects.get(email=email)
        us.delete()
        request.session.flush()
        alert="<script>alert('Account Deleted Successfully');window.location.href='/';</script>"
        return HttpResponse(alert)                                                                                                                                                                      
    else:
        return redirect('investorlogin') 

def edit(request,eid):
    edit=founderregisration.objects.get(id=eid)
    if request.method=="POST":
        name=request.POST.get('name')
        image=request.FILES.get('image')
        password=request.POST.get('password')
        business=request.POST.get('business')
        bio=request.POST.get('bio')
        edit.username=name
        edit.business=business
        edit.password=password
        edit.bio=bio
        if image is not None:
            edit.profilepic=image
        
        edit.save()
        return redirect('/founder_pro/')
   
    return render(request,'founder_proedit.html',{'edit':edit})

def investoredit(request,eid):
    edit=investorregistration.objects.get(id=eid)
    if request.method=="POST":
        name=request.POST.get('username')
        image=request.FILES.get('image')
        password=request.POST.get('password')
        interested_sectors=request.POST.get('interested_sectors')
        bio=request.POST.get('bio')
        edit.interested_sectors=interested_sectors
        edit.bio=bio
        edit.username=name
        edit.password=password
        if image is not None:
            edit.profilepic=image
        
        edit.save()
        return redirect('/inprofile/')
   
    return render(request,'investoredit.html',{'edit':edit})

def delete(request):
    if 'email' in request.session:
        email=request.session['email']
        us=founderregisration.objects.get(email=email)
        us.delete()
        request.session.flush()
        return redirect('home')
    else:
        return redirect('login')   
def admin_dashboard(request):
    return render(request,'admin_dashboard.html')
def admin_userlist(request):
    user=registration.objects.all()
    return render(request,'admin_userlist.html',{'usr':user})
# def admin_stafflist(request):
#     staff=moderls.staffsignup.object.all()
#     return render(request,'admin_stafflist.html',{'stf':staff})
from django.contrib.auth.hashers import make_password

def founderregistration(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        businessname = request.POST.get('businessname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        profilepic = request.FILES.get('image')
        bio = request.POST.get('bio')  

        # Hash the password before saving
        hashed_password = make_password(password)

        # Check if email already exists
        if founderregisration.objects.filter(email=email).exists():
            messages.error(request, "This email is already registered. Please use a different email.")
            return render(request, 'founderregistration.html')

        # Save the new user with the hashed password
        founderregisration(username=username, business=businessname, email=email, password=hashed_password,
                           profilepic=profilepic, phone=phone, bio=bio).save()

        messages.success(request, "Successfully Registered!")
        return render(request, 'home.html')
        
    return render(request, 'founderregistration.html')


def founderlist(request):
    user=founderregisration.objects.all()
    return render(request,'founderlist.html',{'usr':user})


def invest(request):
    user=founderregisration.objects.all()
    return render(request,'invest.html',{'investusr':user})


from django.contrib.auth.hashers import check_password

#Founder Login Function
def founderlogin(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        print(username)
        password = request.POST.get('password')
        print(password)
        
        try:
            # Check if the user exists with the provided email
            user = founderregisration.objects.get(email=username)
                # If password matches, set the session email and other user data
            request.session['email'] = user.email
            request.session['user_id'] = user.id  # Store user ID in session
            request.session['username'] = user.username  # Store username if needed
                
                # Redirect the user to their home page
            return redirect('founder_home')  # Ensure the URL name is correct
        except Exception as e:
            print(e)
        
    return render(request, 'founder_login.html')

# Founder Index Page
def founderindex(request):
    if 'email'in request.session:
        mail=request.session['email']
        usr=founderregisration.objects.get(email=mail)
    return render(request,'founder_home.html',{'usr':usr})

def logout(request):
    request.session.flush()
    return render(request,'home.html')


from django.contrib import messages


#invseter registration
def investerregistration(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        profilepic = request.FILES.get('image')
        bio = request.POST.get('bio')
        interested_sectors = request.POST.get('interested_sectors')
        
        # Check if the email already exists
        if investorregistration.objects.filter(email=email).exists():
            # If email already exists, display a message and return to the registration page
            messages.error(request, "This email is already registered. Please use a different email.")
            return render(request, 'investorregistaration.html')
        
        # Create and save the new investorregistration if email is unique
        investorregistration.objects.create(username=username, email=email, password=password, 
                                            profilepic=profilepic, phone=phone, bio=bio, 
                                            interested_sectors=interested_sectors)
        
        messages.success(request, "Successfully Registered")
        return redirect('investorlogin')  # Redirect to the login page after successful registration
        
    return render(request, 'investorregistaration.html')

#Investor Login Function
def investorlogin(request):
    if request.method =='POST':
        username=request.POST.get('email')
        print(username)
        password=request.POST.get('password')
        print(password)
        try:
            user=investorregistration.objects.get(email=username,password=password)
            print("y",user)
            semail=user.email
            request.session['email']=semail
            return redirect('investor_home')
        except Exception as e:
            print("h",e)
            msg="invalid password or email"
            return render(request,'investor_login.html',{"msg":msg})
    return render(request,'investor_login.html')

# investor index page:
# def investor_home(request):
#     if 'email'in request.session:
#         mail=request.session['email']
#         usr=investorregistration.objects.get(email=mail)
#     return render(request,'investor_home.html',{'usr':usr})

def profile(request):
    if 'email' in request.session:
        mail=request.session['email']
        u=investorregistration.objects.get(email=mail)
        return render(request,'investorprofile.html',{'usr':u})
    else:
        return render('investor_home')

# @csrf_protect
# def submit_contact(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         email = request.POST.get('email')
#         message = request.POST.get('message')

#         # Process the data (e.g., send email or save to database)
#         # For simplicity, just return a HttpResponse
#         return HttpResponse(f"Thank you {name}, we have received your message!")

#     # Redirect to the form page with an error or notification if needed
#     return HttpResponse("There was an error with your submission, please go back and try again.")

def investor_home(request):
    if 'email'in request.session:
        mail=request.session['email']
        usr=investorregistration.objects.get(email=mail)
    return render(request,'investor_home.html',{'usr':usr})

def founder_home(request):
    return render(request,'founder_home.html')


def founder_profile(request):
    if 'email' in request.session:
        email = request.session['email']
        try:
            founder = founderregisration.objects.get(email=email)
        except:
            founder = None
        return render(request, 'founder_pro.html', {'founder': founder})
    else:
        return redirect('founder_login')
      
def investlist(request):
    # Get the current logged-in user's email (or adjust this according to your login system)
    email = request.session.get('email')  # Assuming you're using session-based login for simplicity
    
    # Get the investor object using the email
    investor = investorregistration.objects.get(email=email)
    
    # Get all investments related to this investor
    investments = Investment.objects.filter(user=investor).select_related('startup')

    return render(request, 'investlist.html', {'investments': investments, 'investor': investor})

def investorslist(request):
    inves=investorregistration.objects.all()
    return render(request,'investorslist.html',{'inv':inves})

def deleteinvest(request,iid):
    investorregistration.objects.get(id=iid).delete()
    return redirect('investlist')

def investors(request):
    inv=investorregistration.objects.all()
    return render(request,'investors.html',{'inv':inv})


def sell(request,id):
        
        if 'email' in request.session:
            email = request.session['email']

def investnamedetails(request):
    email = request.session.get('email')
    investor = get_object_or_404(investorregistration, email=email)
    investments = Investment.objects.filter(user=investor)

    return render(request, 'investments_list.html', {
        'investments': investments
    })



#chatsection

def chat_list(request):
    investors = investorregistration.objects.all()  # Replaced 'artists' with 'investors'
    founders = founderregisration.objects.all()  # Replaced 'buyers' with 'founders'
    return render(request, 'chat_list.html', {'investors': investors, 'founders': founders})


from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from .models import founderregisration, investorregistration, ChatMessage

def chat_detail(request, user_type, username):
    sender_email = request.session.get('email')

    if not sender_email:
        return redirect('login')  # If not logged in, redirect to login

    sender = None
    # Get the sender (the logged-in user) from either model
    if investorregistration.objects.filter(email=sender_email).exists():
        sender = investorregistration.objects.get(email=sender_email)
    elif founderregisration.objects.filter(email=sender_email).exists():
        sender = founderregisration.objects.get(email=sender_email)

    if not sender:
        return redirect('login')  # If sender can't be identified, redirect to login

    # Fetch the receiver user based on the user_type and username
    if user_type == 'investor':
        receiver = get_object_or_404(investorregistration, username=username)
    elif user_type == 'founder':
        receiver = get_object_or_404(founderregisration, username=username)
    else:
        raise Http404("User type not recognized")

    # Get messages between the sender and receiver
    messages = ChatMessage.objects.filter(
        sender__in=[sender.username, username],
        receiver__in=[sender.username, username]
    ).order_by('timestamp')

    # Handle sending a message
    if request.method == 'POST':
        content = request.POST.get('content')
        media = request.FILES.get('media')

        if content.strip() or media:
            ChatMessage.objects.create(
                sender=sender.username,
                receiver=username,
                content=content,
                media=media if media else None
            )

        return redirect('chat_detail', user_type=user_type, username=username)

    return render(request, 'chat_detail.html', {
        'receiver': receiver,
        'messages': messages,
        'sender': sender
    })

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Startup

# View to display all startups
def view_startups(request):
    startups = Startup.objects.all()
    return render(request, 'startuplist.html', {'startups': startups})


def view_startups_user(request):
    sender_email = request.session.get('email')
    
    if not sender_email:
        return redirect('founderlogin')
    
    startups = Startup.objects.filter(user__email=sender_email)
    
    return render(request, 'startup_list_user.html', {'startups': startups})

# View to add a new startup without using a form
def add_startup(request):
    email=request.session.get('email')
    if email:
        user=founderregisration.objects.get(email=email)
    if request.method == 'POST':
        name = request.POST.get('name')
        logo = request.FILES.get('logo') 
        bio = request.POST.get('bio')
        description = request.POST.get('description')
        stockprice=request.POST.get('stockprice')
        totalstock=request.POST.get('totalstock')

        if name and logo and bio and description:
            # Create the new startup
            startup = Startup.objects.create(
                user=user,
                name=name,
                logo=logo,
                bio=bio,
                description=description,
                stockprice=stockprice,
                totalstock=totalstock
            )
            return redirect('view_startups')  # Redirect to the list of startups
        else:
            return HttpResponse("All fields are required.", status=400)

    return render(request, 'addstartup.html')


# views.py
import razorpay
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
from .models import Startup
from django.views.decorators.csrf import csrf_exempt
import json

# Initialize Razorpay client
razorpay_client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

@csrf_exempt
def handle_payment(request, startupid):
    try:
        startup = Startup.objects.get(id=startupid)
    except Startup.DoesNotExist:
        return JsonResponse({"error": "Startup not found"}, status=404)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Load the JSON request body
            num_stocks = int(data.get('numStocks'))  # Get the number of stocks from the request

            if num_stocks <= 0 or num_stocks > startup.totalstock:
                return JsonResponse({"error": "Invalid number of stocks"}, status=400)

            total_amount = startup.stockprice * num_stocks * 100  # Razorpay expects amount in paise

            # Create a Razorpay order
            order = razorpay_client.order.create({
                'amount': total_amount,
                'currency': 'INR',
                'payment_capture': '1'
            })
            order_id = order['id']

            return JsonResponse({
                'order_id': order_id,
                'startup_name': startup.name,
                'total_amount': total_amount / 100  # Convert back to INR for display
            })

        except Exception as e:
            return JsonResponse({"error": f"Error: {str(e)}"}, status=400)
    else:
        return JsonResponse({"error": "Invalid request method. Only POST is allowed."}, status=405)
    


razorpay_client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

@csrf_exempt
def verify_payment(request):
    if request.method == 'POST':
        try:
            # Load the JSON data from the request body
            data = json.loads(request.body)
            payment_id = data.get('razorpay_payment_id')
            order_id = data.get('razorpay_order_id')
            signature = data.get('razorpay_signature')

            # Verify the payment signature
            razorpay_client.utility.verify_payment_signature({
                'razorpay_order_id': order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            })

            # Fetch payment details from Razorpay
            payment = razorpay_client.payment.fetch(payment_id)
            startup_id = data.get('startup_id')
            num_stocks = int(data.get('num_stocks'))
            user_id = data.get('user_id')  # Investor (user) ID
            email = request.session.get('email')  # Fetching the email from the session

            # Fetch the startup and investor using email
            startup = Startup.objects.get(id=startup_id)
            investor = investorregistration.objects.get(email=email)  # Query using email

            # Check if the startup has enough stocks available
            if startup.totalstock >= num_stocks:
                # Reduce the stocks of the startup
                startup.totalstock -= num_stocks
                startup.stockprice+=((num_stocks/startup.totalstock)*100)*(startup.stockprice/100)
                startup.save()  

                # Create the Payment record to store the payment details
                payment_record = Payment.objects.create(
                    payment_id=payment_id,
                    razorpay_order_id=order_id,
                    amount=payment['amount'] / 100,  # Convert from paise to INR
                    status='success',
                    investor=investor,
                    startup=startup
                )

                # Create the Investment record to store the investment details
                investment_record = Investment.objects.create(
                    user=investor,  # Use the investor object, not just the id
                    startup=startup,
                    num_stocks=num_stocks,
                    total_investment=payment['amount'] / 100,  # Convert to INR
                    payment=payment_record
                )

                # Return success response or redirect to the success page
                return render(request, 'successpayment.html', {'startup_name': startup.name, 'num_stocks': num_stocks})

            else:
                # If there are not enough stocks, return an error
                return JsonResponse({"error": "Not enough stocks available."}, status=400)

        except razorpay.errors.SignatureVerificationError:
            return JsonResponse({"error": "Payment verification failed"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request method."}, status=405)

#founder profile edit


#startup list edit for user

def startupedit(request,eid):
    edit=Startup.objects.get(id=eid)
    if request.method == "POST":
        startup_id = request.POST.get('startup_id')
        name = request.POST.get('name')
        bio = request.POST.get('bio')
        description = request.POST.get('description')
        stockprice = request.POST.get('stockprice')
        totalstock = request.POST.get('totalstock')
        logo = request.FILES.get('logo')

        try:
            startup = Startup.objects.get(id=startup_id)
            startup.name = name
            startup.bio = bio
            startup.description = description  # Make sure to save the description
            startup.stockprice = stockprice
            startup.totalstock = totalstock
            if logo:
                startup.logo = logo
            startup.save()
            return redirect('/view_startups_user/')
        except Startup.DoesNotExist:
            return HttpResponse("Startup not found", status=404)
            
    return render(request,'startupseditfounder.html',{'edit':edit})

def startupdelete(request, eid):
    startup = get_object_or_404(Startup, id=eid)

    if request.method == "POST":
        startup.delete()
        return redirect('view_startups_user')  # Redirect after successful deletion
    
    return render(request, 'startup_confirm_delete.html', {'startup': startup})

def about(request):
    """
    This view handles the rendering of the 'About' page for StartFund.
    """
    return render(request, 'about.html')

def fodelete(request):
    if 'email'in request.session:
        mail=request.session['email']
        usr=founderregistration.objects.get(email=mail)
        return render(request,'fodelete.html',{'usr':usr})
    return redirect('/founder_login/')



from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Investment, Paymen  # Use Paymen as per your model name

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Investment, Paymen  # Ensure the correct import

from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from .models import Investment, Paymen
from .models import investorregistration

from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from .models import Investment, Paymen
from .models import investorregistration,Paymentmodel

def sell_investment(request, investment_id):
    email = request.session.get('email')  # Assuming you're using session-based login for simplicity
    print(f"Email: {email}")
    
    # Get the investor object using the email
    investor = get_object_or_404(investorregistration, email=email)
    print(f"Investor: {investor}")
    
    # Get all investments for this investor
    investments = Investment.objects.filter(user=investor)
    print(f"All Investments for Investor: {investments}")
    
    # Get the specific investment object by investment_id
    investment = get_object_or_404(Investment, id=investment_id, user=investor)
    print(f"Investment: {investment}")
    print('line 711',investment.total_investment)
    
    
    try:
        # Create a new Paymen object
        p = Paymentmodel(
            email=email,
            investment=investment,
            amount_received=investment.total_investment,  # Assuming the full investment amount is paid back
            status='Completed',  # Adjust the status as needed
            # You can add a transaction ID or anything else if needed
            
        )
        print('line 723 mmm',investment.total_investment)
        print('investment at line 720',investment)

        
        # Save the Paymen object
        p.save()
        print(p)

        
        # Now delete the investment after payment is saved
        investment.delete()
        
        # Add a success message for the user
        messages.success(request, f'Your investment in {investment.startup.name} has been sold successfully.')
        
        return redirect('investlist')  # Redirect to the invest list page after the operation

    except Exception as e:
        # Log or print the error for debugging
        print(f"Error: {e}")
        messages.error(request, "An error occurred while selling your investment.")
        return redirect('investlist')  # Optionally, redirect back to the investment list on error


def amt(request):
    if 'email' in request.session:
        email=request.session['email']
        amt=Paymentmodel.objects.filter(email=email)
        return render(request,'amt.html',{'amt':amt})
    else:
        return redirect('investor_login')