from django.shortcuts import render
from donation_app.models import FoodDonation
from user_app.models import UserProfile
from ngo_app.models import NGOMedia
from django.contrib import messages
from django.shortcuts import redirect

# def dashboard(request):
#     total = FoodDonation.objects.count()
#     collected = FoodDonation.objects.filter(status='Collected').count()
#     return render(request, 'admin_app/dashboard.html', {'total': total, 'collected': collected})


# from django.contrib.admin.views.decorators import staff_member_required

# @staff_member_required
def admin_dashboard(request):
    donations = FoodDonation.objects.all().order_by('-donation_id')
    users = UserProfile.objects.all()
    media_list = NGOMedia.objects.all().order_by('-uploaded_at')
    return render(request, 'admin_dashboard.html', {
        'donations': donations,
        'users': users,
        'media_list': media_list,
    })


def delete_media(request, media_id):
    media = NGOMedia.objects.get(id=media_id)
    media.delete()
    messages.success(request, 'Media deleted successfully.')
    return redirect('admin_dashboard')


def delete_donation(request, donation_id):
    FoodDonation.objects.filter(donation_id=donation_id).delete()
    messages.success(request, 'Donation deleted successfully.')
    return redirect('admin_dashboard')


def delete_user(request, user_id):
    UserProfile.objects.filter(id=user_id).delete()
    messages.success(request, 'User deleted successfully.')
    return redirect('admin_dashboard')

def edit_donation(request, donation_id):
    donation = FoodDonation.objects.get(donation_id=donation_id)
    if request.method == "POST":
        donation.food_name = request.POST['food_name']
        donation.quantity = request.POST['quantity']
        donation.expiry_time = request.POST['expiry_time']
        donation.save()
        return render(request, 'admin_dashboard.html', {'message': 'Donation updated successfully.'})
    return render(request, 'edit_donation.html', {'donation': donation})

def edit_user(request, user_id):
    user = UserProfile.objects.get(id=user_id)
    if request.method == "POST":
        user.user.username = request.POST['username']
        user.user.email = request.POST['email']
        user.role = request.POST['role']
        user.save()
        return render(request, 'admin_dashboard.html', {'message': 'User updated successfully.'})
    return render(request, 'edit_user.html', {'user': user})

def view_donation(request, donation_id):
    donation = FoodDonation.objects.get(donation_id=donation_id)
    return render(request, 'view_donation.html', {'donation': donation})

def view_user(request, user_id):
    user = UserProfile.objects.get(id=user_id)
    return render(request, 'view_user.html', {'user': user})

def search_donations(request):
    query = request.GET.get('q')
    donations = FoodDonation.objects.filter(food_name__icontains=query)
    return render(request, 'admin_dashboard.html', {'donations': donations})

def search_users(request):
    query = request.GET.get('q')
    users = UserProfile.objects.filter(user__username__icontains=query)
    return render(request, 'admin_dashboard.html', {'users': users})

def filter_donations(request):
    status = request.GET.get('status')
    donations = FoodDonation.objects.filter(status=status)
    return render(request, 'admin_dashboard.html', {'donations': donations})

def filter_users(request):
    role = request.GET.get('role')
    users = UserProfile.objects.filter(role=role)
    return render(request, 'admin_dashboard.html', {'users': users})

def sort_donations(request):
    sort_by = request.GET.get('sort_by')
    donations = FoodDonation.objects.all().order_by(sort_by)
    return render(request, 'admin_dashboard.html', {'donations': donations})

def sort_users(request):
    sort_by = request.GET.get('sort_by')
    users = UserProfile.objects.all().order_by(sort_by)
    return render(request, 'admin_dashboard.html', {'users': users})

