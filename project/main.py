import os
from flask import Flask, render_template
from application.config import LocalDevelopmentConfig, TestingConfig
from application.database import db
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

app = Flask(__name__, template_folder="templates",static_folder='static')
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

#app = None

def create_app():
    if os.getenv('ENV', "development") == "production":
        app.logger.info("Currently no production config is setup")
        raise Exception("Currently no production config is setup.")
    elif os.getenv('ENV','development')=="testing":
        app.logger.info('Starting Testing')
        app.config.from_object(TestingConfig)
    else:
        app.logger.info("Starting local development")
        print("Starting Local Development")
        app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    migrate=Migrate(app,db)
    login_manager.login_view = "log"
    login_manager.login_message_category = "info"
    app.app_context().push()
    
    app.logger.info("App setup complete")
    return app

app = create_app()



from application.controllers import *

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

if __name__ == '__main__':
    
    app.run(host='0.0.0.0', port=8080, debug=True)
