from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import FoodDonation, DonationMessage
from django.utils import timezone
from django.contrib import messages


# from django.contrib import messages

@login_required
def verify_pickup(request):
    if request.method == "POST":
        code = request.POST.get('code')

        donation = FoodDonation.objects.filter(
            short_id=code,
            status='Claimed',
            ngo=request.user
        ).first()

        if donation:
            donation.status = 'Collected'
            donation.collected_at = timezone.now()
            donation.save()
            messages.success(request, "Pickup verified successfully!")
            return redirect('ngo_history')

        messages.error(request, "Invalid Code or not authorized.")

    return render(request, 'verify.html')



def donation_detail(request, donation_id):
    donation = get_object_or_404(FoodDonation, donation_id=donation_id)
    msgs = DonationMessage.objects.filter(donation=donation).order_by('created_at')

    # handle sending new message
    if request.method == 'POST' and request.user.is_authenticated:
        # only donor or claiming NGO can message
        if request.user == donation.donor or request.user == donation.ngo:
            body = request.POST.get('body', '').strip()
            if body:
                DonationMessage.objects.create(
                    donation=donation,
                    sender=request.user,
                    text=body
                )
                return redirect('donation_detail', donation_id=donation_id)
    return render(request, 'donation_detail.html', {'donation': donation, 'messages_list': msgs})
