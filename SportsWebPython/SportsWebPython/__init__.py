"""
The flask application package.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

Sportsapp = Flask(__name__)
Sportsapp.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
Sportsapp.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/SportDB'
db = SQLAlchemy(Sportsapp)

#Instance connection name: aerial-chimera-211120:europe-west2:sporteventdb
#Instance ID : sporteventdb
#mysql+mysqldb://root@/<dbname>?unix_socket=/cloudsql/<projectid>:<instancename>
bcrypt = Bcrypt(Sportsapp)


   
import SportsWebPython.views

