from flask.views import MethodView
from . import admin
from src.controllers import AdminController


class Admin_view(MethodView):
    """ Class to open up all other admin routes"""
    
    def get(self):
        """ Fetch template holding buttons to fetch other admin views of forms"""
        return AdminController.admin()
    
    
class VendorView(MethodView):
    """ Class to conduct all vendor get and post actions"""
    
    def get(self):
        """ Fetch vendor creation template form"""
        return AdminController.create_vendor()
    
    def post(self):
        """Submit vendor creation form"""
        return AdminController.create_vendor()
    
      
class AllVendorsView(MethodView):
    """ Fetch all vendors"""
    
    def get(self):
        return AdminController.vendors()
    
    
# define API resources
admin_view = Admin_view.as_view('admin_view')
vendor_view = VendorView.as_view('vendor_view')
all_vendors_view = AllVendorsView.as_view('all_vendors_view')

# add url_rule for endpoints
admin.add_url_rule(
    '/admin',
    view_func=admin_view
)
admin.add_url_rule(
    '/create-vendor',
    view_func=vendor_view
)
admin.add_url_rule(
    '/subaccounts',
    view_func=all_vendors_view
)