from django.shortcuts import render
from .forms import CustomUserCreationForm , ReservationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
# Create your views here.
from .models import Product
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Cart, CartItem, Order, OrderItem
from .models import Reservation, TimeSlot
from django.core.mail import send_mail
from django.conf import settings
import logging

# 產品首頁
@login_required(login_url='/register/')
def product_list(request):
    # 從數據庫中獲取所有 Product 對象
    products = Product.objects.all()
    # 渲染模板 'store/product_list.html'，並傳遞產品列表給模板
    return render(request, 'store/product_list.html', {'products': products})
# 關於我們
def about(request):
    return render(request, 'store/about.html')




@login_required(login_url='/register/')
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    cart_item.quantity +=1
    cart_item.save()        
    return redirect('product_list')

@login_required(login_url='/register/')
def view_cart(request):
    cart=Cart.objects.get(user=request.user)
    total_price = sum([item.product.price * item.quantity for item in cart.cartitem_set.all()])
    return render(request,'store/view_cart.html', {'cart': cart, 'total_price': total_price})

@login_required(login_url='/register/')
def checkout(request):
    cart = Cart.objects.get(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart.cartitem_set.all())
    if request.method == 'POST':
        # 模擬收到的付款通知，假設訂單已成功支付
        order = Order.objects.create(user=request.user, total_price=total_price)
        for item in cart.cartitem_set.all():
            OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)
        cart.cartitem_set.all().delete()  # 清空購物車
        return redirect('order_success')  # 將用戶重定向到訂單成功頁面

    return render(request, 'store/checkout.html', {'cart': cart, 'total_price': total_price})

@login_required(login_url='/register/')
def order_success(request):
    return render(request, 'store/order_success.html')


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            user.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_approved:
                login(request, user)
                if user.學生:
                    return redirect('student_home')
                elif user.軍人:
                    return redirect('teacher_home')
                else:
                    return redirect('success1')
            else:
                return render(request, 'login.html', {'form': form, 'error': 'Account not approved yet.'})
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def student_home(request):
    return render(request, 'student_home.html')

@login_required
def teacher_home(request):  
    return render(request, 'teacher_home.html')

@login_required
def success1(request):  
    return render(request, 'success1.html')


logger = logging.getLogger(__name__)

@login_required(login_url='/register/')
def make_reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.save()

            # 获取用户的电子邮件地址
            user_email = request.user.email
            reservation_date = reservation.time_slot.date
            reservation_time = reservation.time_slot.start_time
            reservation_num= reservation.number_of_people
            # 管理員的電子郵件地址
            admin_email = 'l9856978@gmail.com'

            # 发送电子邮件
            email_subject = '預約成功'
            email_message = f'客人 {request.user.username}，\n\n已預約。\n日期: {reservation_date}\n時間: {reservation_time}\n\n共{reservation_num}人！'

            try:
                send_mail(
                    email_subject,
                    email_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [user_email,admin_email],
                    fail_silently=False,
                )
                logger.info(f'Email sent successfully to {user_email}')
                email_sent = 1
            except Exception as e:
                logger.error(f'Error sending email: {e}')
                email_sent = 0

            return redirect('reservation_success', email_sent=email_sent)

    else:
        form = ReservationForm()    


    time_slots = TimeSlot.objects.all()
    return render(request, 'store/make_reservation.html', {'form': form, 'time_slots': time_slots})

def reservation_success(request, email_sent):
    email_sent = bool(int(email_sent))  # 將傳遞的值轉換為布爾值
    return render(request, 'store/reservation_success.html', {'email_sent': email_sent})