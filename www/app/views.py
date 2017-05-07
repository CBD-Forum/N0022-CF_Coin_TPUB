
from flask import render_template, request

from www.app import datass,datas

from www.app import app

@app.route('/')

@app.route('/index')
def index():
    return render_template("index.html")
@app.route('/blocks')
def blocks():
    blocks = datass.get_blocks()
    return render_template("blocks.html", blocks = blocks)
	
@app.route('/block')
#display a block's details by hash
def block():
    block_hash = request.args.get('block_hash')
    block = datass.get_block_info(block_hash)
    return render_template("block.html", block = block)
    
@app.route('/wallet')
#display personal infomation
def wallet():
    my_keys = datass.get_keys()
    my_txs = datass.get_my_txs()
#     my_utxos = get_my_utxos()
#     launched_projects = get_i_launched()
#     participated_projects = get_i_participated()
#     
    return render_template("wallet.html", my_keys = my_keys, my_txs = my_txs) #, my_utxos = my_utxos, launched_projects = launched_projects, participated_projects = participated_projects)

 
@app.route('/indextest')
def indextest():
    blocks = datas.get_blocks()
    return render_template("index.html", blocks = blocks)
    
@app.route('/blocktest')
#display a block's details by hash
def blocktest():
    block_hash = request.args.get('block_hash')
    block = datas.get_block_info(block_hash)
    return render_template("block.html", block = block)
    
@app.route('/wallettest')
#display personal infomation
def wallettest():
    my_keys = datas.get_keys()
    my_txs = datas.get_my_txs()
#     my_utxos = get_my_utxos()
#     launched_projects = get_i_launched()
#     participated_projects = get_i_participated()
#     
    return render_template("wallet.html", my_keys = my_keys, my_txs = my_txs) #, my_utxos = my_utxos, launched_projects = launched_projects, participated_projects = participated_projects)
       