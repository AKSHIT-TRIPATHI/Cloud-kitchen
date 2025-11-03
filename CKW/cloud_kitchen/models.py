from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.conf import settings

class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    password = models.CharField(max_length=128)  # Store hashed password
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    is_staff = models.BooleanField(default=False)  # For admin access
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.username

class Category(models.Model):
    CATEGORY_CHOICES = [
        ('starters', 'Starters & Snacks'),
        ('main_course', 'Main Course'),
        ('biryani', 'Biryani & Rice'),
        ('burgers', 'Burgers & Fast Food'),
        ('drinks', 'Drinks & Beverages'),
        ('desserts', 'Desserts & Ice Creams'),
        ('combos', 'Combos & Meal Boxes'),
    ]

    name = models.CharField(max_length=50, choices=CATEGORY_CHOICES, unique=True)
    display_name = models.CharField(max_length=100)
    emoji = models.CharField(max_length=10, blank=True)
    slug = models.SlugField(unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.display_name

    class Meta:
        verbose_name_plural = "Categories"

class FoodItem(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='food_items')
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    icon_class = models.CharField(max_length=50, help_text="FontAwesome icon class (e.g., 'fas fa-hamburger')")
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - ₹{self.price}"

    class Meta:
        ordering = ['created_at']

class Cart(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart for {self.user.username if self.user else 'Anonymous'}"

    def get_total_items(self):
        return sum(item.quantity for item in self.cartitem_set.all())

    def get_subtotal(self):
        return sum(item.get_total_price() for item in self.cartitem_set.all())

    def get_delivery_fee(self):
        from decimal import Decimal
        return Decimal('40.00')

    def get_tax(self):
        from decimal import Decimal
        return round(self.get_subtotal() * Decimal('0.18'), 2)  # 18% GST

    def get_total(self):
        return self.get_subtotal() + self.get_delivery_fee() + self.get_tax()

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    # Track if this item was added from an offer
    is_offer_item = models.BooleanField(default=False)
    offer_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)

    class Meta:
        unique_together = ['cart', 'food_item']

    def __str__(self):
        return f"{self.quantity}x {self.food_item.name}"

    def get_total_price(self):
        if self.is_offer_item and self.offer_price:
            return self.quantity * self.offer_price
        return self.quantity * self.food_item.price

class Offer(models.Model):
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE, related_name='offers')
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=40.00, help_text="Discount percentage (e.g., 40.00 for 40%)")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.discount_percentage}% off on {self.food_item.name}"

    def get_discounted_price(self):
        from decimal import Decimal
        discount = (self.discount_percentage / Decimal('100')) * self.food_item.price
        return round(self.food_item.price - discount, 2)

    class Meta:
        ordering = ['-created_at']

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('preparing', 'Preparing'),
        ('ready', 'Ready for Pickup'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey('User', on_delete=models.CASCADE)
    order_number = models.CharField(max_length=20, unique=True)
    items = models.JSONField()  # Store cart items as JSON
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=40.00)
    tax = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    delivery_address = models.TextField(blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    special_instructions = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.order_number} - {self.user.username}"

    def save(self, *args, **kwargs):
        if not self.order_number:
            # Generate order number
            import random
            import string
            from datetime import datetime
            order_number = 'CKW' + datetime.now().strftime('%Y%m%d') + ''.join(random.choices(string.digits, k=4))
            self.order_number = order_number
        super().save(*args, **kwargs)
class ContactMessage(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.name} - {self.subject}"

    class Meta:
        ordering = ['-created_at']

class Review(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    message = models.TextField()
    stars = models.PositiveIntegerField(choices=[(i, f"{i} Star{'s' if i > 1 else ''}") for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} - {self.stars} stars"

    class Meta:
        ordering = ['-created_at']
