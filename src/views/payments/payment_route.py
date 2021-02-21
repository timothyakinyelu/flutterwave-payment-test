from flask.views import MethodView
from . import payment
from src.controllers import PaymentController


class PaymentView(MethodView):
    """ Class handling customer payments to sub_accounts 
        through the main merchant account on Flutterwave.
    """ 
    
    def get(self):
        """Fetch donation form to load to users
            in order to make payments.
        """
        return PaymentController.payments()
    
    def post(self):
        """Send form payload to flutterwave payments API gateway
            for payment processing and user security information.
        """
        return PaymentController.payments()
    

class VerificationView(MethodView):
    """ Verify payment parameters. """
    
    def get(self):
        """ Get redirect url included in transaction request payload."""
        return PaymentController.verify_payment()
    
    
# define API resources here
payment_view = PaymentView.as_view('payment_view')
verification_view = VerificationView.as_view('verification_view')

# register url_rule for endpoint
payment.add_url_rule(
    '/payment',
    view_func=payment_view
)
payment.add_url_rule(
    '/verify_transaction',
    view_func=verification_view
)

