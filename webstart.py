"""
URL routing & initialization for webapp
"""

import os
from os.path import join
from main import app
from flask import send_from_directory, Blueprint, send_file

print "Starting webapp!"

# admin pannel
from admin.views import register_admin
register_admin(app)

# splash
from splash.views import splash
app.register_blueprint(splash)

# modules manage their own static files. This serves them all up.
@app.route("/<blueprint_name>/static/<path:fn>")
def _return_static(blueprint_name, fn='index.html'):
    path = join(*app.blueprints[blueprint_name].import_name.split('.')[:-1])
    return send_file('%s/static/%s' % (path, fn)) 

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, port=port)
