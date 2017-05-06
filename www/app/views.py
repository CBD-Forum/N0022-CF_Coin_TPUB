
from flask import render_template, request

from www.app import datass

from www.app import app

@app.route('/')
@app.route('/index')
def index():
    blocks = datass.get_blocks()
    return render_template("index.html", blocks = blocks)
	
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
    