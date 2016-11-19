from flask import (Flask, render_template, Response, request, flash,
    Blueprint, redirect, send_from_directory, send_file, jsonify, g, url_for)
from flask_login import login_user, logout_user, current_user, login_required
from user.models import *
from service.models import *
from datetime import datetime
from main import login_manager
from main import app
service_user = Blueprint('service_user', __name__, template_folder="templates")

