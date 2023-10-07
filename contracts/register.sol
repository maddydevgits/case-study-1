// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

contract register {
  
  address[] _usernames;
  uint[] _passwords;
  string[] _names;

  mapping(address=>bool) _users;

  function signup(address username,uint password,string memory name) public {

    require(!_users[username]);

    _usernames.push(username);
    _passwords.push(password);
    _names.push(name);

    _users[username]=true;
  }

  function viewUsers() public view returns(address[] memory, uint[] memory, string[] memory){
    return (_usernames,_passwords,_names);
  }

  function login(address username,uint password) public view returns(bool){

    uint i;

    for(i=0;i<_usernames.length;i++){
      if(_usernames[i]==username && _passwords[i]==password){
        return true;
      }
    }
    return false;
  }
}
