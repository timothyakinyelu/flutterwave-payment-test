from flask.views import MethodView
from . import user
from src.controllers import PaymentController, UserController


class RegistrationView(MethodView):
    """ Class to register a new user on the application"""
    
    def get(self):
        """ Fetch new user form"""
        return UserController.Register()

    def post(self):
        """ Submit new user form"""
        return UserController.Register()


class LoginView(MethodView):
    """ Class to login a user into the application. """
    
    def get(self):
        """ Fetch new user form"""
        return UserController.Login()
    
    def post(self):
        """ Submit new user form"""
        return UserController.Login()



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
register_view = RegistrationView.as_view('register_view')
login_view = LoginView.as_view('login_view')
payment_view = PaymentView.as_view('payment_view')
verification_view = VerificationView.as_view('verification_view')

# register url_rule for endpoint
user.add_url_rule(
    '/',
    view_func=login_view
)
user.add_url_rule(
    '/register',
    view_func=register_view
)
user.add_url_rule(
    '/payment',
    view_func=payment_view
)
user.add_url_rule(
    '/verify_transaction',
    view_func=verification_view
)

