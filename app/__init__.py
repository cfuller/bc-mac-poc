import os
import time
from flask import Flask, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)

# Configurations
app.config.from_object('config')

Bootstrap(app)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

from app.main.controllers import main as main_module
app.register_blueprint(main_module)
