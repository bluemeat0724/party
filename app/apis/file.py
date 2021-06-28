from . import api
from flask import send_from_directory




@api.route('/<filename>')
def uploaded_file(filename):
    return send_from_directory('static',
                               filename)