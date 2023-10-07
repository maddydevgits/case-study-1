// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

contract chat {
  
  string[] _msgs;
  address[] _senders;
  address[] _receivers;

  function addMessage(address sender,address receiver,string memory message)public{

    _msgs.push(message);
    _senders.push(sender);
    _receivers.push(receiver);
  }

  function viewMessages() public view returns(string[] memory,address[] memory,address[] memory){
    return(_msgs,_senders,_receivers);
  }
}
