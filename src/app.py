from flask import Flask,render_template,request, session,redirect
from web3 import Web3,HTTPProvider
import json

blockchainServer='http://127.0.0.1:7545'

chat_artifact_path='../build/contracts/chat.json'
register_artifact_path='../build/contracts/register.json'

def connect_with_register(walletaddr):
    web3=Web3(HTTPProvider(blockchainServer))
    web3.eth.defaultAccount=walletaddr

    with open(register_artifact_path) as f:
        register_artifact=json.load(f)
        register_abi=register_artifact['abi']
        register_contract_address=register_artifact['networks']['5777']['address']
    
    contract=web3.eth.contract(address=register_contract_address,abi=register_abi)
    return contract,web3

def connect_with_chat(walletaddr):
    web3=Web3(HTTPProvider(blockchainServer))
    web3.eth.defaultAccount=walletaddr

    with open(chat_artifact_path) as f:
        chat_artifact=json.load(f)
        chat_abi=chat_artifact['abi']
        chat_contract_address=chat_artifact['networks']['5777']['address']
    
    contract=web3.eth.contract(address=chat_contract_address,abi=chat_abi)
    return contract,web3

frontend=Flask(__name__) 
frontend.secret_key='m@dhu'

@frontend.route('/')
def homePage():
    return render_template('index.html')

@frontend.route('/register')
def registerPage():
    return render_template('register.html')

@frontend.route('/login')
def loginPage():
    return render_template('login.html')

@frontend.route('/signupform',methods=['post'])
def signupform():
    name=request.form['name']
    walletaddr=request.form['walletaddr']
    password=int(request.form['password'])
    print(name,walletaddr,password)
    try:
        contract,web3=connect_with_register(walletaddr)
        tx_hash=contract.functions.signup(walletaddr,password,name).transact()
        web3.eth.waitForTransactionReceipt(tx_hash)
        return (render_template('register.html',response='Account Created Successfully'))
    except:
        return (render_template('register.html',response='Account exist'))

@frontend.route('/loginform',methods=['post'])
def loginform():
    walletaddr=request.form['walletaddr']
    password=int(request.form['password'])
    print(walletaddr,password)
    try:
        contract,web3=connect_with_register(walletaddr)
        state=contract.functions.login(walletaddr,password).call()
        if state==True:
            session['username']=walletaddr
            return redirect('/dashboard')
        else:
            return render_template('login.html',response='Invalid Login')
    except:
        return render_template('login.html',response='login error')

@frontend.route('/dashboard')
def dashboardPage():
    return render_template('dashboard.html')

@frontend.route('/logout')
def logoutPage():
    session['username']=''
    return redirect('/')

@frontend.route('/composeform',methods=['post'])
def composeform():
    message=request.form['message']
    walletaddr=request.form['walletaddr']
    print(message,walletaddr)
    contract,web3=connect_with_chat(session['username'])
    tx_hash=contract.functions.addMessage(session['username'],walletaddr,message).transact()
    web3.eth.waitForTransactionReceipt(tx_hash)
    return render_template('dashboard.html',response='Message Sent')

@frontend.route('/inbox')
def inboxPage():
    contract,web3=connect_with_chat(session['username'])
    _msgs,_senders,_receivers=contract.functions.viewMessages().call()
    data=[]
    for i in range(len(_msgs)):
        if(_receivers[i]==session['username']):
            dummy=[]
            dummy.append(_senders[i])
            dummy.append(_msgs[i])
            data.append(dummy)

    return render_template('inbox.html',data=data,l=len(data))

@frontend.route('/sent')
def sentPage():
    contract,web3=connect_with_chat(session['username'])
    _msgs,_senders,_receivers=contract.functions.viewMessages().call()
    data=[]
    for i in range(len(_msgs)):
        if(_senders[i]==session['username']):
            dummy=[]
            dummy.append(_receivers[i])
            dummy.append(_msgs[i])
            data.append(dummy)
            
    return render_template('sent.html',data=data,l=len(data))

if __name__=="__main__":
    frontend.run(
        host='0.0.0.0',
        port=5001,
        debug=True
    )