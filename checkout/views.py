from django.shortcuts import render, reverse, redirect
from django.contrib import messages
from .forms import OrderForm
from shoppingbag.contexts import bag_contents
from django.conf import settings

import stripe

# Create your views here.
# checkour view
def checkout(request):
    # create stripe payment intent
    # public key
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    #secret key
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    # get the bag from the session
    bag = request.session.get('bag', {})
    # if statment for logic around if bag is empty
    if not bag:
        messages.error(request, "Your bag is currently empty")
        return redirect(reverse('products'))

    # create new variable for stripe payments so the old one is not overridden
    current_bag = bag_contents(request)
    # getting the total key from the current bag
    total = current_bag['grand_total']
    # round the total for stripe
    stripe_total = round(total * 100)
    # setting secret key on stripe
    stripe.api_key = stripe_secret_key
    # createing the payment intent
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
    )

    # creating the order form instance
    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        # add stripe secret key
        'stripe_public_key': 'pk_test_51M1CYYGLT9eFji1UAXkz1tcBoXIzozeKbxP3j2Tf31pRfj8qD2bcczgQjwfMCQEC3el0XZYIY4CBY7oaRKvaXp9w00XkO37pJh',
        'client_secret': 'test client secret',
    }

    # renders out the order form
    return render(request, template, context)