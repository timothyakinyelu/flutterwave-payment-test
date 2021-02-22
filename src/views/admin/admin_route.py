from flask.views import MethodView
from . import admin


class Admin_view(MethodView):
    """ Class to open up all other admin routes"""
    
    def get(self):
        """ Fetch template holding buttons to fetch other admin views of forms"""
        pass
    
    
# define API resources
admin_view = Admin_view.as_view('admin_view')

# add url_rule for endpoints
admin.add_url_rule(
    '/admin',
    view_func=admin_view
)