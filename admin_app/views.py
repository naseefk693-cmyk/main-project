from django.shortcuts import render
from donation_app.models import FoodDonation

# def dashboard(request):
#     total = FoodDonation.objects.count()
#     collected = FoodDonation.objects.filter(status='Collected').count()
#     return render(request, 'admin_app/dashboard.html', {'total': total, 'collected': collected})


from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def admin_dashboard(request):
    donations = FoodDonation.objects.all().order_by('-id')
    users = UserProfile.objects.all()
    return render(request, 'admin_dashboard.html', {'donations': donations, 'users': users})
