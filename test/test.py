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

# Create an account
# try:
#     contract,web3=connect_with_register('0x84696DF29559bc5381c957d3dCfe4830E87b31db')
#     tx_hash=contract.functions.signup('0x84696DF29559bc5381c957d3dCfe4830E87b31db',1234,'Madhu').transact()
#     web3.eth.waitForTransactionReceipt(tx_hash)
#     print('Account created successfully')
# except:
#     print('Account already exist')

# View Users 
# contract,web3=connect_with_register('0x84696DF29559bc5381c957d3dCfe4830E87b31db')
# _usernames,_passwords,_names=contract.functions.viewUsers().call()

# for i in range(len(_usernames)):
#     print('username: ',_usernames[i])
#     print('password: ',_passwords[i])
#     print('name: ',_names[i])

# Login 

# contract,web3=connect_with_register('0x84696DF29559bc5381c957d3dCfe4830E87b31db')
# status=contract.functions.login('0xA50B4b0B96911d4DaFcaC3267E48bd7d91B5e671',1234).call()
# print(status)

# Add Message

# contract,web3=connect_with_chat('0x84696DF29559bc5381c957d3dCfe4830E87b31db')
# tx_hash=contract.functions.addMessage('0x84696DF29559bc5381c957d3dCfe4830E87b31db','0x2B8Cd3dD825355b65b4325d15B49cd921aC78673','Hi How are you doing').transact()
# web3.eth.waitForTransactionReceipt(tx_hash)
# print('Msg sent')

# View Messages
# contract,web3=connect_with_chat('0x84696DF29559bc5381c957d3dCfe4830E87b31db')
# _msgs,_senders,_receivers=contract.functions.viewMessages().call()

# for i in range(len(_msgs)):
#     print('message: ',_msgs[i])
#     print('sender: ',_senders[i])
#     print('receiver: ',_receivers[i])