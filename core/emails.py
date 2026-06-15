import resend
from django.conf import settings

resend.api_key = settings.RESEND_API_KEY


def send_welcome_email(user):
    try:
        resend.Emails.send({
            "from": "DigitalDrop <onboarding@resend.dev>",
            "to": [user.email],
            "subject": "Welcome to DigitalDrop! 🎉",
            "html": f"""
            <h2>Hi {user.first_name}!</h2>
            <p>Welcome to <strong>DigitalDrop</strong> — the marketplace for digital creators!</p>
            <p>You can now:</p>
            <ul>
                <li>✅ Browse thousands of digital products</li>
                <li>✅ Add products to your wishlist</li>
                <li>✅ Purchase and download instantly</li>
                <li>✅ Sell your own digital products</li>
            </ul>
            <p><a href="https://web-production-ecb5.up.railway.app">Get started →</a></p>
            <p>— The DigitalDrop Team</p>
            """
        })
    except Exception as e:
        print(f"Welcome email error: {e}")


def send_order_confirmation(order):
    try:
        items_html = ''.join([f'<li>{i.product_name} — ${i.product_price}</li>' for i in order.items.all()])
        resend.Emails.send({
            "from": "DigitalDrop <onboarding@resend.dev>",
            "to": [order.buyer_email],
            "subject": f"Order Confirmed — {order.order_number} 📦",
            "html": f"""
            <h2>Your order is confirmed! 🎉</h2>
            <p>Hi {order.buyer_name},</p>
            <p>Your files are ready to download.</p>
            <p><strong>Order:</strong> {order.order_number}</p>
            <p><strong>Total:</strong> ${order.total}</p>
            <h3>Items:</h3>
            <ul>{items_html}</ul>
            <p><a href="https://web-production-ecb5.up.railway.app">Download your files →</a></p>
            <p>— The DigitalDrop Team</p>
            """
        })
    except Exception as e:
        print(f"Order confirmation email error: {e}")


def send_seller_sale_notification(seller, order, item):
    try:
        resend.Emails.send({
            "from": "DigitalDrop <onboarding@resend.dev>",
            "to": [seller.email],
            "subject": f"🎉 You made a sale! — {item.product_name}",
            "html": f"""
            <h2>You made a sale! 🎉</h2>
            <p>Hi {seller.first_name},</p>
            <p><strong>Product:</strong> {item.product_name}</p>
            <p><strong>Amount:</strong> ${item.product_price}</p>
            <p><strong>Order:</strong> {order.order_number}</p>
            <p><strong>Buyer:</strong> {order.buyer_name}</p>
            <p><a href="https://web-production-ecb5.up.railway.app">View your dashboard →</a></p>
            <p>— The DigitalDrop Team</p>
            """
        })
    except Exception as e:
        print(f"Seller notification email error: {e}")


def send_password_reset_email(user, reset_link):
    try:
        resend.Emails.send({
            "from": "DigitalDrop <onboarding@resend.dev>",
            "to": [user.email],
            "subject": "Reset your DigitalDrop password 🔐",
            "html": f"""
            <h2>Reset your password</h2>
            <p>Hi {user.first_name},</p>
            <p>Click the link below to set a new password:</p>
            <p><a href="{reset_link}">Reset Password →</a></p>
            <p>This link expires in 1 hour.</p>
            <p>— The DigitalDrop Team</p>
            """
        })
    except Exception as e:
        print(f"Password reset email error: {e}")