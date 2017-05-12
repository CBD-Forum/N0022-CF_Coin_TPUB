#!flask/bin/python
import random
import sys

from socketInfo.CoinSocket import ReivSocket, SendSocket
from www.app import app


sys.path.append('.')
sys.path.append('..')



SendSocket.init()
app.run(debug = True)
