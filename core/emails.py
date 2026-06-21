import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from django.conf import settings


def get_brevo_client():
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = settings.BREVO_API_KEY
    return sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))


def send_email(to_email, to_name, subject, html):
    try:
        api = get_brevo_client()
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=[{"email": to_email, "name": to_name}],
            sender={"name": "DigitalDrop", "email": "javeriarazzaq15@gmail.com"},
            subject=subject,
            html_content=html
        )
        api.send_transac_email(send_smtp_email)
    except ApiException as e:
        print(f"Email error: {e}")
    except Exception as e:
        print(f"Email error: {e}")


def send_welcome_email(user):
    send_email(
        user.email, user.first_name,
        "Welcome to DigitalDrop! 🎉",
        f"""
        <h2>Hi {user.first_name}!</h2>
        <p>Welcome to <strong>DigitalDrop</strong> — the marketplace for digital creators!</p>
        <ul>
            <li>✅ Browse thousands of digital products</li>
            <li>✅ Purchase and download instantly</li>
            <li>✅ Sell your own digital products</li>
        </ul>
        <p><a href="https://web-production-ecb5.up.railway.app">Get started →</a></p>
        <p>— The DigitalDrop Team</p>
        """
    )


def send_order_confirmation(order):
    items_html = ''.join([f'<li>{i.product_name} — ${i.product_price}</li>' for i in order.items.all()])
    send_email(
        order.buyer_email, order.buyer_name,
        f"Order Confirmed — {order.order_number} 📦",
        f"""
        <h2>Your order is confirmed! 🎉</h2>
        <p>Hi {order.buyer_name},</p>
        <p><strong>Order:</strong> {order.order_number}</p>
        <p><strong>Total:</strong> ${order.total}</p>
        <h3>Items:</h3>
        <ul>{items_html}</ul>
        <p><a href="https://web-production-ecb5.up.railway.app">Download your files →</a></p>
        <p>— The DigitalDrop Team</p>
        """
    )


def send_seller_sale_notification(seller, order, item):
    send_email(
        seller.email, seller.first_name,
        f"🎉 You made a sale! — {item.product_name}",
        f"""
        <h2>You made a sale! 🎉</h2>
        <p>Hi {seller.first_name},</p>
        <p><strong>Product:</strong> {item.product_name}</p>
        <p><strong>Amount:</strong> ${item.product_price}</p>
        <p><strong>Buyer:</strong> {order.buyer_name}</p>
        <p><a href="https://web-production-ecb5.up.railway.app">View dashboard →</a></p>
        <p>— The DigitalDrop Team</p>
        """
    )


def send_password_reset_email(user, reset_link):
    send_email(
        user.email, user.first_name,
        "Reset your DigitalDrop password 🔐",
        f"""
        <h2>Reset your password</h2>
        <p>Hi {user.first_name},</p>
        <p>Click the link below to set a new password:</p>
        <p><a href="{reset_link}">Reset Password →</a></p>
        <p>This link expires in 1 hour.</p>
        <p>— The DigitalDrop Team</p>
        """
    )


def send_review_notification(seller, product, review):
    send_email(
        seller.email, seller.first_name,
        f"⭐ New review on {product.name}",
        f"""
        <h2>You got a new review! ⭐</h2>
        <p>Hi {seller.first_name},</p>
        <p><strong>Product:</strong> {product.name}</p>
        <p><strong>Rating:</strong> {'⭐' * review.rating}</p>
        <p><strong>Review:</strong> "{review.text}"</p>
        <p><a href="https://web-production-ecb5.up.railway.app">View on DigitalDrop →</a></p>
        <p>— The DigitalDrop Team</p>
        """
    )