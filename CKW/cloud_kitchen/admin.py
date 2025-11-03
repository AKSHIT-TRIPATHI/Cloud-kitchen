from django.contrib import admin
from django.urls import reverse, path
from django.utils.html import format_html
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import User, Category, FoodItem, Cart, CartItem, Order, Offer, ContactMessage, Review

# Custom Admin Classes

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ('food_item', 'quantity', 'get_total_price')
    can_delete = False

    def get_total_price(self, obj):
        return f"₹{obj.get_total_price()}"
    get_total_price.short_description = "Total Price"

class CartAdmin(admin.ModelAdmin):
    list_display = ('get_user', 'get_total_items', 'get_subtotal', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'session_key')
    inlines = [CartItemInline]
    readonly_fields = ('created_at', 'updated_at')

    def get_user(self, obj):
        if obj.user:
            return obj.user.username
        return f"Anonymous ({obj.session_key[:8]}...)"
    get_user.short_description = "User"

    def get_total_items(self, obj):
        return obj.get_total_items()
    get_total_items.short_description = "Items Count"

    def get_subtotal(self, obj):
        return f"₹{obj.get_subtotal()}"
    get_subtotal.short_description = "Subtotal"

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'cart_link')
    list_filter = ('is_staff',)
    search_fields = ('username', 'email')

    def cart_link(self, obj):
        try:
            cart = Cart.objects.get(user=obj)
            url = reverse('admin:cloud_kitchen_cart_change', args=[cart.id])
            return format_html('<a href="{}">View Cart ({})</a>', url, cart.get_total_items())
        except Cart.DoesNotExist:
            return "No Cart"
    cart_link.short_description = "Cart"

class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user', 'total', 'status', 'created_at', 'mark_delivered_action')
    list_filter = ('status', 'created_at')
    search_fields = ('order_number', 'user__username')
    list_editable = ('status',)
    actions = ['mark_orders_delivered']

    def mark_delivered_action(self, obj):
        if obj.status != 'delivered':
            return format_html(
                '<a class="button" href="{}" style="background: #417690; color: white; padding: 5px 10px; text-decoration: none; border-radius: 3px;">Mark Delivered</a>',
                reverse('admin:mark_order_delivered', args=[obj.pk])
            )
        return "✅ Delivered"
    mark_delivered_action.short_description = "Action"

    def mark_orders_delivered(self, request, queryset):
        updated = queryset.update(status='delivered')
        self.message_user(request, f'{updated} order(s) marked as delivered.')
    mark_orders_delivered.short_description = "Mark selected orders as delivered"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('mark-delivered/<int:order_id>/', self.mark_delivered_view, name='mark_order_delivered'),
        ]
        return custom_urls + urls

    def mark_delivered_view(self, request, order_id):
        try:
            order = Order.objects.get(pk=order_id)
            order.status = 'delivered'
            order.save()
            self.message_user(request, f'Order {order.order_number} marked as delivered.')
        except Order.DoesNotExist:
            self.message_user(request, 'Order not found.', level='error')

        return HttpResponseRedirect(reverse('admin:cloud_kitchen_order_changelist'))

# Register your models here.

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'stars', 'message_preview', 'created_at')
    list_filter = ('stars', 'created_at')
    search_fields = ('user__username', 'message')
    readonly_fields = ('created_at',)

    def message_preview(self, obj):
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    message_preview.short_description = "Message Preview"

admin.site.register(User, UserAdmin)
admin.site.register(Category)
admin.site.register(FoodItem)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem)
admin.site.register(Offer)
admin.site.register(ContactMessage)
admin.site.register(Order, OrderAdmin)
admin.site.register(Review, ReviewAdmin)
