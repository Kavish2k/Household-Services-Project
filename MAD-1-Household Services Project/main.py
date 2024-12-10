from flask import Flask
from application.database import db
app=Flask(__name__,template_folder= 'templates',static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///household_serv_database.sqlite3"
db.init_app(app)
app.app_context().push()


from application.controllers import*


if __name__=='__main__':
    app.run(debug=True)




