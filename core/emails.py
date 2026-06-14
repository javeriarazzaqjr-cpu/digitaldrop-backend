from django.core.mail import send_mail
from django.conf import settings


def send_welcome_email(user):
    send_mail(
        subject='Welcome to DigitalDrop! 🎉',
        message=f'''Hi {user.first_name},

Welcome to DigitalDrop — the marketplace for digital creators!

You can now:
✅ Browse thousands of digital products
✅ Add products to your wishlist
✅ Purchase and download instantly
✅ Sell your own digital products

Get started: https://web-production-ecb5.up.railway.app

— The DigitalDrop Team
''',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=True,
    )


def send_order_confirmation(order):
    items_text = '\n'.join([f'  - {i.product_name} (${i.product_price})' for i in order.items.all()])
    send_mail(
        subject=f'Order Confirmed — {order.order_number} 📦',
        message=f'''Hi {order.buyer_name},

Your order has been confirmed and your files are ready to download!

Order: {order.order_number}
Total: ${order.total}

Items:
{items_text}

Log in to your account to download your files:
https://web-production-ecb5.up.railway.app

Thank you for shopping on DigitalDrop!

— The DigitalDrop Team
''',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[order.buyer_email],
        fail_silently=True,
    )


def send_seller_sale_notification(seller, order, item):
    send_mail(
        subject=f'🎉 You made a sale! — {item.product_name}',
        message=f'''Hi {seller.first_name},

Great news — someone just bought your product!

Product: {item.product_name}
Amount: ${item.product_price}
Order: {order.order_number}
Buyer: {order.buyer_name}

Check your dashboard for details:
https://web-production-ecb5.up.railway.app

Keep it up! 🚀

— The DigitalDrop Team
''',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[seller.email],
        fail_silently=True,
    )


def send_password_reset_email(user, reset_link):
    send_mail(
        subject='Reset your DigitalDrop password 🔐',
        message=f'''Hi {user.first_name},

We received a request to reset your password.

Click the link below to set a new password:
{reset_link}

This link expires in 1 hour. If you didn't request this, ignore this email.

— The DigitalDrop Team
''',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=True,
    )