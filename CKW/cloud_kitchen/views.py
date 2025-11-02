from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .models import User, Category, FoodItem, Cart, CartItem, Order, Offer, ContactMessage, Review
import random
import string

def login_view(request):
    if request.method == 'POST':
        username_or_email = request.POST.get('username')
        password = request.POST.get('password')

        # Find user by username or email
        user = User.objects.filter(username=username_or_email).first() or User.objects.filter(email=username_or_email).first()

        if user and user.check_password(password):
            request.session['user_id'] = user.id
            request.session['username'] = user.username
            # Check if user is staff/admin and redirect accordingly
            if user.is_staff:
                return redirect('/admin/')
            else:
                return redirect('home')
        else:
            messages.error(request, 'Invalid username/email or password')
            return redirect('login')

    return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return redirect('register')

        user = User(username=username, email=email)
        user.set_password(password)
        user.save()

        messages.success(request, 'Registration successful! Please login.')
        return redirect('login')

    return render(request, 'register.html')

def home_view(request):
    username = request.session.get('username')
    if not username:
        return redirect('login')
    return render(request, 'home.html', {'username': username})

def forgot_password_view(request):
    if request.method == 'POST':
        if 'send_otp' in request.POST:
            username_or_email = request.POST.get('username_email')

            # Check if user exists by username or email
            user = User.objects.filter(username=username_or_email).first() or User.objects.filter(email=username_or_email).first()

            if not user:
                messages.error(request, 'User not found with this username or email')
                return redirect('forgot_password')

            # Generate 4-digit OTP
            otp = ''.join(random.choices(string.digits, k=4))

            # Store OTP in session (in production, use a more secure method)
            request.session['reset_otp'] = otp
            request.session['reset_user_id'] = user.id

            # Show OTP on page (no popup alert)
            return render(request, 'forgot_password.html', {'otp_sent': True, 'username_email': username_or_email, 'otp': otp})

        elif 'reset_password' in request.POST:
            otp = request.POST.get('otp')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')

            # Verify OTP
            stored_otp = request.session.get('reset_otp')
            user_id = request.session.get('reset_user_id')

            if not stored_otp or not user_id:
                messages.error(request, 'Session expired. Please try again.')
                return redirect('forgot_password')

            if otp != stored_otp:
                messages.error(request, 'Invalid OTP')
                return render(request, 'forgot_password.html', {'otp_sent': True})

            if new_password != confirm_password:
                messages.error(request, 'Passwords do not match')
                return render(request, 'forgot_password.html', {'otp_sent': True})

            # Update password
            try:
                user = User.objects.get(id=user_id)
                user.set_password(new_password)
                user.save()

                # Clear session
                del request.session['reset_otp']
                del request.session['reset_user_id']

                messages.success(request, 'Password reset successfully! Please login with your new password.')
                return redirect('login')
            except User.DoesNotExist:
                messages.error(request, 'User not found')
                return redirect('forgot_password')

    return render(request, 'forgot_password.html')

def menu_view(request):
    username = request.session.get('username')
    if not username:
        return redirect('login')
    return render(request, 'menu.html', {'username': username})

def drinks_view(request):
    username = request.session.get('username')
    if not username:
        return redirect('login')

    # Get food items from database
    try:
        category = Category.objects.get(slug='drinks')
        food_items = FoodItem.objects.filter(category=category, is_available=True)
    except Category.DoesNotExist:
        food_items = []

    return render(request, 'drinks.html', {
        'username': username,
        'food_items': food_items
    })

def starters_view(request):
    username = request.session.get('username')
    if not username:
        return redirect('login')

    # Get food items from database
    try:
        category = Category.objects.get(slug='starters')
        food_items = FoodItem.objects.filter(category=category, is_available=True)
    except Category.DoesNotExist:
        food_items = []

    return render(request, 'starters.html', {
        'username': username,
        'food_items': food_items
    })

def main_course_view(request):
    username = request.session.get('username')
    if not username:
        return redirect('login')

    # Get food items from database
    try:
        category = Category.objects.get(slug='main_course')
        food_items = FoodItem.objects.filter(category=category, is_available=True)
    except Category.DoesNotExist:
        food_items = []

    return render(request, 'main_course.html', {
        'username': username,
        'food_items': food_items
    })

def biryani_view(request):
    username = request.session.get('username')
    if not username:
        return redirect('login')

    # Get food items from database
    try:
        category = Category.objects.get(slug='biryani')
        food_items = FoodItem.objects.filter(category=category, is_available=True)
    except Category.DoesNotExist:
        food_items = []

    return render(request, 'biryani.html', {
        'username': username,
        'food_items': food_items
    })

def burgers_view(request):
    username = request.session.get('username')
    if not username:
        return redirect('login')

    # Get food items from database
    try:
        category = Category.objects.get(slug='burgers')
        food_items = FoodItem.objects.filter(category=category, is_available=True)
    except Category.DoesNotExist:
        food_items = []

    return render(request, 'burgers.html', {
        'username': username,
        'food_items': food_items
    })

def desserts_view(request):
    username = request.session.get('username')
    if not username:
        return redirect('login')

    # Get food items from database
    try:
        category = Category.objects.get(slug='desserts')
        food_items = FoodItem.objects.filter(category=category, is_available=True)
    except Category.DoesNotExist:
        food_items = []

    return render(request, 'desserts.html', {
        'username': username,
        'food_items': food_items
    })

def combos_view(request):
    username = request.session.get('username')
    if not username:
        return redirect('login')

    # Get food items from database
    try:
        category = Category.objects.get(slug='combos')
        food_items = FoodItem.objects.filter(category=category, is_available=True)
    except Category.DoesNotExist:
        food_items = []

    return render(request, 'combos.html', {
        'username': username,
        'food_items': food_items
    })

def get_or_create_cart(request):
    """Get or create cart for the current user/session"""
    user_id = request.session.get('user_id')

    if user_id:
        # User is logged in with custom authentication
        try:
            user = User.objects.get(id=user_id)
            cart, created = Cart.objects.get_or_create(user=user)
        except User.DoesNotExist:
            # Fallback to session-based cart if user not found
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
                session_key = request.session.session_key
            cart, created = Cart.objects.get_or_create(session_key=session_key)
    else:
        # For anonymous users, use session key
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key)
    return cart

def cart_view(request):
    username = request.session.get('username')
    if not username:
        return redirect('login')

    cart = get_or_create_cart(request)
    cart_items = []

    for item in cart.cartitem_set.all():
        cart_items.append({
            'id': item.id,
            'name': item.food_item.name,
            'description': item.food_item.description,
            'price': item.food_item.price,
            'icon_class': item.food_item.icon_class,
            'quantity': item.quantity,
            'total_price': item.get_total_price()
        })

    # Calculate totals
    subtotal = cart.get_subtotal()
    delivery_fee = cart.get_delivery_fee()
    tax = cart.get_tax()
    total = cart.get_total()

    context = {
        'username': username,
        'cart_items': cart_items,
        'subtotal': subtotal,
        'delivery_fee': delivery_fee,
        'tax': tax,
        'total': total
    }

    return render(request, 'cart.html', context)

def add_to_cart(request, item_id):
    """AJAX endpoint to add item to cart"""
    if request.method == 'POST':
        try:
            food_item = FoodItem.objects.get(id=item_id, is_available=True)
            cart = get_or_create_cart(request)

            # Check if this is being added from offers page (check for offer parameter)
            is_offer_item = request.POST.get('is_offer', 'false').lower() == 'true'

            # Get offer price if it's an offer item
            offer_price = None
            if is_offer_item:
                try:
                    offer = Offer.objects.get(food_item=food_item, is_active=True)
                    offer_price = offer.get_discounted_price()
                except Offer.DoesNotExist:
                    offer_price = None

            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                food_item=food_item,
                defaults={
                    'quantity': 1,
                    'is_offer_item': is_offer_item,
                    'offer_price': offer_price
                }
            )

            if not created:
                cart_item.quantity += 1
                # Update offer status if adding to existing item
                if is_offer_item and not cart_item.is_offer_item:
                    cart_item.is_offer_item = True
                    cart_item.offer_price = offer_price
                cart_item.save()

            return JsonResponse({'success': True, 'message': 'Item added to cart'})
        except FoodItem.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Item not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Invalid request method'})

def update_cart_item(request, item_id):
    """AJAX endpoint to update cart item quantity"""
    if request.method == 'POST':
        try:
            action = request.POST.get('action')
            cart = get_or_create_cart(request)
            cart_item = CartItem.objects.get(id=item_id, cart=cart)

            if action == 'increase':
                cart_item.quantity += 1
            elif action == 'decrease' and cart_item.quantity > 1:
                cart_item.quantity -= 1

            cart_item.save()

            # Return updated totals
            return JsonResponse({
                'success': True,
                'quantity': cart_item.quantity,
                'item_total': float(cart_item.get_total_price()),
                'subtotal': float(cart.get_subtotal()),
                'tax': float(cart.get_tax()),
                'total': float(cart.get_total())
            })

        except CartItem.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Item not found in cart'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Invalid request method'})

def remove_from_cart(request, item_id):
    """AJAX endpoint to remove item from cart"""
    if request.method == 'POST':
        try:
            cart = get_or_create_cart(request)
            cart_item = CartItem.objects.get(id=item_id, cart=cart)
            cart_item.delete()

            return JsonResponse({
                'success': True,
                'subtotal': float(cart.get_subtotal()),
                'tax': float(cart.get_tax()),
                'total': float(cart.get_total())
            })

        except CartItem.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Item not found in cart'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Invalid request method'})

def profile_view(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        # Handle profile picture upload
        if 'profile_pic' in request.FILES:
            user.profile_pic = request.FILES['profile_pic']

        # Handle email, phone number, and address updates
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        if email:
            user.email = email
        if phone_number:
            user.phone_number = phone_number
        user.address = address  # Address can be empty

        user.save()
        messages.success(request, 'Profile updated successfully!')
        # Clear any existing messages to prevent accumulation
        storage = messages.get_messages(request)
        storage.used = True
        return redirect('profile')
    return render(request, 'profile.html', {'user': user})

def logout_view(request):
    # Clear the user session
    request.session.flush()

def track_view(request):
    username = request.session.get('username')
    if not username:
        return redirect('login')

    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)

    # Get user's orders, latest first
    orders = Order.objects.filter(user=user).order_by('-created_at')

    context = {
        'username': username,
        'orders': orders
    }

    return render(request, 'track.html', context)
def contact_view(request):
    username = request.session.get('username')
    if not username:
        return redirect('login')

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Get current user if logged in
        user_id = request.session.get('user_id')
        user = None
        if user_id:
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                user = None

        # Save contact message
        ContactMessage.objects.create(
            user=user,
            name=name,
            email=email,
            subject=subject,
            message=message
        )

        messages.success(request, 'Your message has been sent successfully! We will get back to you soon.')
        return redirect('contact')

    return render(request, 'contact.html', {'username': username})

def reviews_view(request):
    username = request.session.get('username')
    if not username:
        return redirect('login')

    # Get latest 4 reviews for display
    latest_reviews = Review.objects.select_related('user').order_by('-created_at')[:4]

    context = {
        'username': username,
        'latest_reviews': latest_reviews
    }
    return render(request, 'reviews.html', context)

def submit_review(request):
    """API endpoint to submit a review"""
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        if not user_id:
            return JsonResponse({'success': False, 'message': 'User not logged in'})

        try:
            user = User.objects.get(id=user_id)
            message = request.POST.get('message', '').strip()
            stars = request.POST.get('stars')

            if not message:
                return JsonResponse({'success': False, 'message': 'Message cannot be empty'})

            if not stars or not stars.isdigit() or not (1 <= int(stars) <= 5):
                return JsonResponse({'success': False, 'message': 'Please select a valid rating (1-5 stars)'})

            # Create the review
            review = Review.objects.create(
                user=user,
                message=message,
                stars=int(stars)
            )

            return JsonResponse({
                'success': True,
                'message': 'Review submitted successfully!',
                'review': {
                    'id': review.id,
                    'user': user.username,
                    'profile_pic': user.profile_pic.url if user.profile_pic else None,
                    'message': review.message,
                    'stars': review.stars,
                    'created_at': review.created_at.strftime('%Y-%m-%d %H:%M:%S')
                }
            })

        except User.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'User not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Invalid request method'})

def get_reviews(request):
    """API endpoint to get latest 4 reviews"""
    try:
        reviews = Review.objects.select_related('user').order_by('-created_at')[:4]
        reviews_data = []

        for review in reviews:
            reviews_data.append({
                'id': review.id,
                'user': review.user.username,
                'profile_pic': review.user.profile_pic.url if review.user.profile_pic else None,
                'message': review.message,
                'stars': review.stars,
                'created_at': review.created_at.strftime('%Y-%m-%d %H:%M:%S')
            })

        return JsonResponse({'success': True, 'reviews': reviews_data})

    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

def about_view(request):
    username = request.session.get('username')
    if not username:
        return redirect('login')
    return render(request, 'about.html', {'username': username})

    return redirect('login')

def offers_view(request):
    username = request.session.get('username')
    if not username:
        return redirect('login')

    # Get all active offers with food items
    offers = Offer.objects.filter(is_active=True).select_related('food_item')

    offer_items = []
    for offer in offers:
        offer_items.append({
            'id': offer.id,
            'food_item_id': offer.food_item.id,
            'name': offer.food_item.name,
            'description': offer.food_item.description,
            'original_price': offer.food_item.price,
            'discounted_price': offer.get_discounted_price(),
            'discount_percentage': offer.discount_percentage,
            'icon_class': offer.food_item.icon_class,
            'is_available': offer.food_item.is_available
        })

    context = {
        'username': username,
        'offer_items': offer_items
    }

    return render(request, 'offers.html', context)

def order_confirmation_view(request):
    username = request.session.get('username')
    if not username:
        return redirect('login')

    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    cart = get_or_create_cart(request)

    # Check if cart has items
    if not cart.cartitem_set.exists():
        return redirect('cart')

    # Check if this is a POST request (from cart pay button)
    if request.method == 'POST':
        # Prepare order items data
        order_items = []
        for item in cart.cartitem_set.all():
            order_items.append({
                'food_item_id': item.food_item.id,
                'name': item.food_item.name,
                'description': item.food_item.description,
                'price': float(item.food_item.price),
                'quantity': item.quantity,
                'total_price': float(item.get_total_price()),
                'is_offer_item': item.is_offer_item,
                'offer_price': float(item.offer_price) if item.offer_price else None
            })

        # Calculate totals
        subtotal = cart.get_subtotal()
        delivery_fee = cart.get_delivery_fee()
        tax = cart.get_tax()
        total = cart.get_total()

        # Create the order
        order = Order.objects.create(
            user=user,
            items=order_items,  # Store as JSON
            subtotal=subtotal,
            delivery_fee=delivery_fee,
            tax=tax,
            total=total,
            status='pending'
        )

        # Clear the cart after successful order creation
        cart.cartitem_set.all().delete()

        # Store order details in session for GET request
        request.session['last_order_id'] = order.id
        request.session['last_order_number'] = order.order_number

        return JsonResponse({'success': True, 'order_id': order.id})

    # GET request - check if we have order details from session
    order_id = request.session.get('last_order_id')
    if order_id:
        try:
            order = Order.objects.get(id=order_id, user=user)
            # Clear session data
            del request.session['last_order_id']
            del request.session['last_order_number']
        except Order.DoesNotExist:
            return redirect('cart')
    else:
        # No order in session, redirect to cart
        return redirect('cart')

    # Prepare order items for template display
    order_items_display = []
    for item in order.items:
        order_items_display.append({
            'name': item['name'],
            'description': item['description'],
            'price': item['price'],
            'icon_class': 'fas fa-utensils',  # Default icon since we don't store it in order
            'quantity': item['quantity'],
            'total_price': item['total_price']
        })

    context = {
        'username': username,
        'order_number': order.order_number,
        'cart_items': order_items_display,  # Reuse cart_items template variable
        'subtotal': order.subtotal,
        'delivery_fee': order.delivery_fee,
        'tax': order.tax,
        'total': order.total
    }

    return render(request, 'order_confirmation.html', context)


