from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import DonationForm, DonationModelForm
from .models import Donate
from django.conf import settings
import stripe

# Create your views here.
stripe.api_key = settings.STRIPE_SECRET

# Create your views here.
@login_required
def donate(request):    
    if request.method=="POST":
        donation_form = DonationForm(request.POST)
        donate_model_form = DonationModelForm(request.POST)
        
        if donate_model_form.is_valid() and donation_form.is_valid():
            donation_model = donate_model_form.save(commit=False) # saves the donation value, we commit false as below we will save the user who donates
            donation_model.user = request.user
            total = donation_model.donation
            donation_model.save()
            
            customer = None
            
            try:
                customer = stripe.Charge.create(
                    amount = int(total * 100),
                    currency = "EUR",
                    description = request.user.username,
                    card = donation_form.cleaned_data['stripe_id'],
                )
            except stripe.error.CardError:
                messages.error(request, "Your card was declined!")
                alertResult = { "result":"danger" }
               
            if customer is not None:  
                alertResult = { "result":"success" }
                if customer.paid:
                    messages.error(request, "You have successfully donated, thank you!")
                    return redirect(reverse("index"))
            else:
                messages.error(request, "Unable to take payment")
                alertResult = { "result":"danger" }
        
        else:
            ''' print(donation_form.errors) '''
            messages.error(request, "We were unable to take a payment with that card!")
            alertResult = { "result":"danger" }
    else:
        donation_form = DonationForm()
        donate_model_form = DonationModelForm()
        alertResult = { "result":"success" }
        
    return render(request, "donate.html", {'donation_form': donation_form, 'donate_model_form': donate_model_form, 'publishable': settings.STRIPE_PUBLISHABLE, 'alertResult': alertResult})
