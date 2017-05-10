from flask import Flask

app = Flask(__name__)
from www.app import views
from www.app import datas

