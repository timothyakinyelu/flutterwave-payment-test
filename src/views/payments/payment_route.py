from flask.views import MethodView
from . import payment

class PaymentView(MethodView):
    """ Class handling customer payments to sub_accounts 
        through the main merchant account on Flutterwave.
    """ 
    
    def get(self):
        """Fetch donation form to load to users
            in order to make payments.
        """
        pass
    
    def post(self):
        """Send form payload to flutterwave payments API gateway
            for payment processing and user security information.
        """
        pass
    
# define API resources here
payment_view = PaymentView.as_view('payment_view')

# register url_rule for endpoint
payment.add_url_rule(
    '/',
    view_func=payment_view
)

