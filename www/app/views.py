from flask import render_template, request

from www.app import datass,datas

from www.app import app
from pycoin.serialize import h2b
import time


ALERT = '''数据解析错误！'''

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

# @app.route('/index')
# def index():
#     return render_template("index.html")
@app.route('/blocks')
def blocks():
    try:
        blocks = datass.get_blocks()
        return render_template("blocks.html", blocks = blocks)
    except Exception:
        return render_template("index.html", alert=ALERT) 
    
@app.route('/block')
#display a block's details by hash
def block():
    try:
        block_hash = request.args.get('block_hash')
        if block_hash == '0'*64 or block_hash in ('', None):
            return render_template("index.html")
        block_hash = h2b(block_hash)
        block = datass.get_block_info(block_hash)
        return render_template("block.html", block = block)
    except Exception:
        return render_template("index.html", alert=ALERT) 
    
@app.route('/wallet', methods = ['GET', ])
#display personal infomation
def wallet():
    try:
        display = request.args.get('display')    
        if display == 'spent':
            my_utxos = datass.get_my_used_out_txs()
        elif display == 'unspent':
            my_utxos = datass.get_my_unused_out_txs()
        else:
            my_utxos = datass.get_my_all_out_txs()
            display = 'all'
        my_keys = datass.get_keys()
        
    #     my_utxos = get_my_utxos()
    #     launched_projects = get_i_launched()
    #     participated_projects = get_i_participated()
    #     
        return render_template("wallet.html", my_keys = my_keys, my_utxos = my_utxos) #, my_utxos = my_utxos, launched_projects = launched_projects, participated_projects = participated_projects)
    except Exception:
        return render_template("index.html", alert=ALERT) 
 
# @app.route('/indextest')
# def indextest():
#     blocks = datas.get_blocks()
#     return render_template("index.html", blocks = blocks)
#     
# @app.route('/blocktest')
# #display a block's details by hash
# def blocktest():
#     block_hash = request.args.get('block_hash')
#     block = datas.get_block_info(block_hash)
#     return render_template("block.html", block = block)
#     
# @app.route('/wallettest')
# #display personal infomation
# def wallettest():
#     try:
#         my_keys = datas.get_keys()
#         my_txs = datas.get_my_txs()
#     #     my_utxos = get_my_utxos()
#     #     launched_projects = get_i_launched()
#     #     participated_projects = get_i_participated()
#     #     
#         return render_template("wallet.html", my_keys = my_keys, my_txs = my_txs) #, my_utxos = my_utxos, launched_projects = launched_projects, participated_projects = participated_projects)
#     except Exception:
#         return render_template("index.html", alert=ALERT) 
    
    
@app.route('/CF_projects')
def CF_projects():
    try:
        projects = datass.get_CF_projects()  
        return render_template("CF_projects.html", projects = projects)  
    except Exception:
        return render_template("index.html", alert=ALERT) 

@app.route('/CF_project_detail')
def CF_project_detail():
    try:
        project_id = request.args.get('CF_project_id')
        project = datass.get_CF_project(project_id)  
        return render_template("CF_project_detail.html", project = project) 
    except Exception:
        return render_template("index.html", alert=ALERT) 

@app.route('/tx') 
def tx():
    try:
        tx_id = request.args.get('tx_id')
        if tx_id == '0'*64 or tx_id in ('', None):
            return render_template("index.html")
        tx = datass.get_tx(h2b(tx_id))  
        return render_template("tx.html", tx = tx) 
    except Exception:
        return render_template("index.html", alert=ALERT) 
    
@app.route('/action', methods = ['GET', 'POST']) 
def action():
    try:
        action = request.form.get('action')
        if not action:
            return render_template("action.html")
        if action == 'createNewCFBitCoinTx':
            target_amount = int(request.form.get('target_amount'))
            pubkey_addr = request.form.get('pubkey_addr')
            end_time = int(time.time() + float(request.form.get('end_time')) * 3600 *24)
            pre_out_ids_for_fee = request.form.get('pre_out_ids_for_fee').split(';')
    #         pre_out_ids_for_fee = [pre_out_ids_for_fee[0], int(pre_out_ids_for_fee[1])]
            res = datass.createNewCFBitCoinTx(target_amount, pubkey_addr, end_time, pre_out_ids_for_fee)
               
          
        elif action == 'createNormalCFBitCoinTx':
            pre_out_ids = [ int(i) for i in request.form.get('pre_out_ids').split(';')]
            pre_cf_hash = h2b(request.form.get('pre_cf_hash')) 
            spendValue = int(request.form.get('spendValue'))
            
            otherPublicAddrToValueArray = []
            addrs = request.form.getlist('otherPublicAddrToValueArray[]') 
            coin_values = request.form.getlist('coin_value[]')
            for pubkey, coin in zip(addrs, coin_values):
                if '' == coin:
                    continue
                otherPublicAddrToValueArray.append([pubkey, int(coin)])
            
            refund_addr = request.form.get('refund_addr') 
            res = datass.createNormalCFBitCoinTx(pre_out_ids, pre_cf_hash, spendValue, otherPublicAddrToValueArray, refund_addr)
            
        elif action == 'createNormalBitCoinTx':
            pre_out_ids = [ int(i) for i in request.form.get('pre_out_ids').split(';')]
            
            publicAddrToValueArray = []
            addrs = request.form.getlist('publicAddrToValueArray[]') 
            coin_values = request.form.getlist('coin_value[]')
            for pubkey, coin in zip(addrs, coin_values):
                publicAddrToValueArray.append([pubkey, int(coin)])
            res = datass.createNormalBitCoinTx(pre_out_ids, publicAddrToValueArray)
            
        elif action == 'createNewBitcoinTx':
            pubkey_addr = request.form.get('pubkey_addr')
            pubkey = request.form.get('publicAddrToValueArray')
            coin = request.form.get('newBotcoinValue')
            res = datass.createNewBitcoinTx([[pubkey, int(coin)]])
    except Exception:
        res = None
    if not res:
        alert = '''交易生成失败！请重新检查参数。'''
    else:
        alert = '''发送成功！交易Id为%s''' % res.hash().hex()
    return render_template("action.html", alert = alert) 

@app.route('/address')
def address():
    return render_template("index.html")



@app.route('/about')
def about():
    return render_template("about.htm")  
    
# @app.route('/demo')
# def demo():
#     return render_template("demo.html")


