#!flask/bin/python
from socketInfo.CoinSocket import ReivSocket, SendSocket
import sys
sys.path.append('.')
sys.path.append('..')

from www.app import app


ReivSocket.init() 
SendSocket.init()
app.run(debug = True)
