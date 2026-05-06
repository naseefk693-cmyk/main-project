from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import UserProfile
from donation_app.models import FoodDonation
from admin_app.views import admin_dashboard

# # Index (public)
# def index_view(request):
#     donations = FoodDonation.objects.filter(status="Available", expiry_time__gt=timezone.now()).order_by('-donation_id')
#     return render(request, 'index.html', {'donations': donations})

from .models import Review, VisitorMessage
from .forms import ReviewForm, VisitorMessageForm
from ngo_app.models import NGOMedia

def index_view(request):
    donations = FoodDonation.objects.filter(
        status="Available", 
        expiry_time__gt=timezone.now()
    ).order_by('-donation_id')


    message_form = VisitorMessageForm(request.POST or None, prefix='message')
    review_form = ReviewForm(request.POST or None, prefix='review')

    if request.method == "POST":
        if 'message-submit' in request.POST and message_form.is_valid():
            message_form.save()
            messages.success(request, "Your message has been sent!")
            return redirect('index')
        elif 'review-submit' in request.POST and review_form.is_valid():
            review_form.save()
            messages.success(request, "Thank you for your review!")
            return redirect('index')

    reviews = Review.objects.all().order_by('-submitted_at')
    ngo_media = NGOMedia.objects.all().order_by('-uploaded_at')  # latest first

    context = {
        'donations': donations,
        'message_form': message_form,
        'review_form': review_form,
        'reviews': reviews,
        'ngo_media': ngo_media,
    }
    return render(request, 'index.html', context)



# Register
def register_view(request):
    from .forms import RegistrationForm
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful! Welcome to ECO-FEED.")
            return redirect('index')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

# Login
# def login_view(request):
#     if request.method == "POST":
#         u = request.POST['username']
#         p = request.POST['password']
#         user = authenticate(username=u, password=p)
#         if user is not None:
#             login(request, user)
#             profile = UserProfile.objects.get(user=user)
#             if profile.role == 'donor':
#                 return redirect('donor_history')
#             else:
#                 return redirect('browse_food')
#         else:
#             messages.error(request, "Invalid username or password.")
#     return render(request, 'login.html')

from django.contrib.auth.models import User

def login_view(request):
    if request.method == "POST":
        u = request.POST['username']
        p = request.POST['password']
        user = authenticate(username=u, password=p)

        if user is not None:
            login(request, user)

            # If admin, go to admin dashboard
            if user.is_superuser:
                return redirect('admin_dashboard')

            profile = UserProfile.objects.filter(user=user).first()

            if profile:
                if profile.role == 'donor':
                    return redirect('donor_history')
                elif profile.role == 'admin':
                    return redirect('admin_dashboard')
                else:
                    return redirect('browse_food')
            else:
                messages.error(request, "User profile not found.")

        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'login.html')

# Logout
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')

# Donor: Create Donation
@login_required(login_url='/user/login/')
def create_donation(request):
    try:
        profile = request.user.userprofile
        if profile.role != 'donor':
            messages.error(request, "Only donors can create donations.")
            return redirect('index')
    except UserProfile.DoesNotExist:
        messages.error(request, "User profile not found.")
        return redirect('index')
        
    if request.method == "POST":
        expiry = request.POST['expiry_time']
        donation =FoodDonation.objects.create(
            donor=request.user,
            food_type=request.POST['food_type'],
            quantity=request.POST['quantity'],
            expiry_time=expiry,
            image=request.FILES.get('image')
        )
        messages.success(request,f"Donation posted successfully! your donation id is {donation.donation_id}")
        return redirect('donor_history')
    return render(request, 'create.html')

# Donor: Edit Unclaimed Donation
@login_required(login_url='/user/login/')
def edit_donation(request, donation_id):
    try:
        profile = request.user.userprofile
        if profile.role != 'donor':
            messages.error(request, "Only donors can edit donations.")
            return redirect('index')
    except UserProfile.DoesNotExist:
        messages.error(request, "User profile not found.")
        return redirect('index')
        
    donation = get_object_or_404(FoodDonation, id=donation_id, donor=request.user, status="Available")
    if request.method == "POST":
        donation.food_type = request.POST['food_type']
        donation.quantity = request.POST['quantity']
        donation.expiry_time = request.POST['expiry_time']
        if request.FILES.get('image'):
            donation.image = request.FILES['image']
        donation.save()
        messages.success(request, "Donation updated successfully!")
        return redirect('donor_history')
    return render(request, 'edit_donation.html', {'donation': donation})

# Donor: History
@login_required(login_url='/user/login/')
def donor_history(request):
    try:
        profile = request.user.userprofile
        if profile.role != 'donor':
            messages.error(request, "Access denied.")
            return redirect('index')
    except UserProfile.DoesNotExist:
        messages.error(request, "User profile not found.")
        return redirect('index')
        
    donations = FoodDonation.objects.filter(donor=request.user).order_by('-donation_id')
    return render(request, 'donor_history.html', {'donations': donations})

# User: Edit Profile
@login_required(login_url='/user/login/')
def edit_profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == "POST":
        profile.address = request.POST['address']
        profile.phone = request.POST['phone']
        profile.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('index')
    return render(request, 'edit_profile.html', {'profile': profile})


@login_required(login_url='/user/login/')
def claim_donation(request, donation_id):
    # simply redirect to the detail page where the NGO can specify quantity
    return redirect('donation_detail', donation_id=donation_id)



# views.py
from django.shortcuts import render, redirect
from .forms import VisitorMessageForm, ReviewForm
from django.contrib import messages

def visitor_contact(request):
    if request.method == "POST":
        form = VisitorMessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your message has been sent!")
            return redirect('visitor_contact')
    else:
        form = VisitorMessageForm()

    return render(request, 'visitor_contact.html', {'form': form})

def visitor_review(request):
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you for your review!")
            return redirect('visitor_review')
    else:
        form = ReviewForm()

    return render(request, 'visitor_review.html', {'form': form})
