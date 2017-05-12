#!flask/bin/python
# from socketInfo.CoinSocket import ReivSocket, SendSocket
from www.app import app


# ReivSocket.init() 
# SendSocket.init()
app.run(debug = True)
