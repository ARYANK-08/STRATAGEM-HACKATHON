import stripe 
from flask import Flask, redirect
auth = Flask(__name__,static_url_path="",static_folder="templates")
 
stripe.api_key = "sk_test_51MmaNCSHVsxclTOVnNtwa3Cc8MZCLdYslMSnEaNd7ZW6Uo9iuLTcHsq75SKTLIqUMkQyODIjppyQH5XG4vFlcxgQ00qevbk9is"
 
YOUR_DOMAIN = "http://localhost:5000"
 
@auth.route('/create-checkout-session',methods=["POST"])
def create_checkout_session():
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items = [
                {
                    "price":"price_1MmaRgSHVsxclTOVXptXXpQo",
                    "quantity":1
                }
            ],
            mode="payment",
            success_url=YOUR_DOMAIN + "/success.html",
            cancel_url = YOUR_DOMAIN + "/cancel.html"
        )
    except Exception as e:
        return str(e)
 
    return redirect(checkout_session.url,code=303)
 
if __name__ == "__main__":
    auth.run(port=5000,debug=True)