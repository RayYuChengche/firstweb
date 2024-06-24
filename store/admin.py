from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Product, Cart, CartItem, Order, OrderItem
from .forms import CustomUserCreationForm
from .models import TimeSlot, Reservation

admin.site.register(Product)

class CartItemInline(admin.TabularInline):
    model = CartItem

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    inlines = [CartItemInline]

class OrderItemInline(admin.TabularInline):
    model = OrderItem

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    model = CustomUser
    list_display = ('username', '學生', '軍人', 'is_approved', 'is_staff')
    list_filter = ('學生', '軍人', 'is_approved')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_approved', '學生', '軍人')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', '學生', '軍人', 'is_approved')}
        ),
    )
    search_fields = ('username',)
    ordering = ('username',)

try:
    admin.site.register(CustomUser, CustomUserAdmin)
except admin.sites.AlreadyRegistered:
    pass

admin.site.register(TimeSlot)
admin.site.register(Reservation)
