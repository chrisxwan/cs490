#SQL ADMIN PANNEL
from main import db, app
from user.models import *
from flask import render_template, abort
from flask_admin import Admin, AdminIndexView, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import login_user, logout_user, current_user, login_required
from wtforms.fields import SelectField
from collections import Counter
import locale

class AdminAccess(object):
    def is_accessible(self):
        user = current_user
        if not user.is_authenticated():
            return abort(404)
        elif user.email in ['christopher.wan@yale.edu', 'chrisxwan@gmail.com']:
            return True
        else:
            return abort(404)

class AdminView(AdminAccess, ModelView):
    page_size = 50

class ReadOnlyView(AdminAccess, ModelView):
    can_create = False
    can_edit = True
    can_delete = False

class DeleteView(AdminAccess, ModelView):
    can_create = False
    can_edit = True
    can_delete = True

class UserView(DeleteView):
    column_list = ('id', 'firstname', 'lastname', 'email', 'email_confirmation_status')
    column_searchable_list = ('firstname', 'lastname', 'email')
    column_labels = {'firstname': 'First',
    				'lastname': 'Last',
    				'email': 'Email',
    				'email_confirmation_status': 'Confirmation Status',
    				'graduation_year': 'Graduation'}
    form_excluded_columns = ('password')
    form_overrides = dict(status=SelectField)
    column_default_sort = ('id')

def register_admin(app):
    admin = Admin(app, name='admin', url='/admin', index_view=AdminIndexView(url='/admin'))
    admin.add_view(UserView(User, db.session))
