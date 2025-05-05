from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Show, Reservation
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.

# View to list all shows
@login_required
def show_list(request):
    shows = Show.objects.all()
    return render(request, 'reservations/show_list.html', {'shows': shows})

# View to create a new show
@login_required
def create_show(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        date = request.POST.get('date')
        location = request.POST.get('location')
        price = request.POST.get('price')
        Show.objects.create(title=title, description=description, date=date, location=location, price=price)
        return redirect('show_list')
    return render(request, 'reservations/create_show.html')

# View to edit a show
@login_required
def edit_show(request, show_id):
    show = Show.objects.get(id=show_id)
    if request.method == 'POST':
        show.title = request.POST.get('title')
        show.description = request.POST.get('description')
        show.date = request.POST.get('date')
        show.location = request.POST.get('location')
        show.price = request.POST.get('price')
        show.save()
        return redirect('show_list')
    return render(request, 'reservations/edit_show.html', {'show': show})

# View to delete a show
@login_required
def delete_show(request, show_id):
    show = Show.objects.get(id=show_id)
    show.delete()
    return redirect('show_list')

# View to handle user registration
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# View to display user profile
@login_required
def profile(request):
    return render(request, 'registration/profile.html')

# View to create a Stripe checkout session
def create_checkout_session(request):
    YOUR_DOMAIN = "http://127.0.0.1:8000"
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': 'Show Ticket',
                },
                'unit_amount': 2000,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=YOUR_DOMAIN + '/success/',
        cancel_url=YOUR_DOMAIN + '/cancel/',
    )
    return JsonResponse({
        'id': checkout_session.id
    })
