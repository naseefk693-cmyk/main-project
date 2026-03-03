from django.shortcuts import render, get_object_or_404, redirect
from donation_app.models import FoodDonation
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from donation_app.models import FoodDonation
from django.contrib import messages
from ngo_app.models import NGO, NGOMedia
from ngo_app.forms import NGOMediaForm



def browse_food(request):
    # Only show food not expired and not yet claimed
    items = FoodDonation.objects.filter(status='Available', expiry_time__gt=timezone.now())
    return render(request, 'browse.html', {'items': items})

def claim_food(request, donation_id):
    item = get_object_or_404(FoodDonation, donation_id=donation_id)
    if item.status == 'Available':
        item.status = 'Claimed'
        item.ngo = request.user
        item.claimed_at = timezone.now()  # optional, if you track claim time
        item.save()
    return redirect('ngo_history')

def ngo_history(request):
    claims = FoodDonation.objects.filter(ngo=request.user)
    return render(request, 'ngo_history.html', {'claims': claims})

@login_required
def verify_pickup(request):
    if request.method == "POST":
        donation_id = request.POST['donation_id']
        donation = get_object_or_404(FoodDonation, donation_id=donation_id, ngo=request.user)
        donation.status = "Collected"
        donation.collected_at = timezone.now()
        donation.save()
        messages.success(request, "Pickup verified successfully!")
        return redirect('ngo_history')
    return render(request, 'verify_pickup.html')


@login_required(login_url='/user/login/')
def upload_ngo_media(request):
    # Ensure user role is NGO
    if request.user.userprofile.role != 'ngo':
        messages.error(request, "Only NGO users can upload media.")
        return redirect('/')

    # Get or create NGO profile
    ngo, created = NGO.objects.get_or_create(
        user=request.user,
        defaults={'name': request.user.username}  # default name if missing
    )

    if request.method == "POST":
        form = NGOMediaForm(request.POST, request.FILES)
        if form.is_valid():
            media = form.save(commit=False)
            media.ngo = ngo  # assign NGO
            media.save()
            messages.success(request, "Media uploaded successfully!")
            return redirect('upload_ngo_media')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = NGOMediaForm()

    return render(request, 'ngo_app/upload_ngo_media.html', {'form': form})





