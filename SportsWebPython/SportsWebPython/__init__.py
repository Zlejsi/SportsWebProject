"""
The flask application package.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/SportDB'
db = SQLAlchemy(app)

#Instance connection name: aerial-chimera-211120:europe-west2:sporteventdb
#Instance ID : sporteventdb
#mysql+mysqldb://root@/<dbname>?unix_socket=/cloudsql/<projectid>:<instancename>
bcrypt = Bcrypt(app)


   
import SportsWebPython.views

