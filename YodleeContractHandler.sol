pragma solidity ^0.4.4;

contract YodleeContractHandler {

    struct UserData {
        address acct;
        uint lastAccess;
        uint dailyPrice;
    }

    mapping (string=>UserData) private users;

    function addUser (address account, string id, uint dailyPrice) public payable {
        users[id] = UserData(account, now, dailyPrice);
    }

    function updateUser (string id, uint newDailyPrice) public payable {
        users[id].dailyPrice = newDailyPrice;
        payUser(id);
    }

    function getUserPrice (string id) public constant returns (uint){
        payUser(id);
        return users[id].dailyPrice;
    }

    function removeUser (string id) public {
        delete users[id];

        //remove our access from Yodlee not currently fully possible, however
        //the library Oraclize would just need to add the ability to pass in
        //an HTTP header, and we could query Yodlee to delete a user account.
        //This ensures that when we want to stop paying because we aren't
        //getting the information we were told we would get, that we also no
        //longer are able to query Yodlee for their data. Ideally, we would
        //create a highly complex smart contract that would handle all
        //Yodlee queries for some price. For this demo at least, we are just
        //removing the user from the payments, and assume the link is lost.
    }

    function payUser (string id) public {
        UserData user = users[id];
        uint newTime = now;
        uint oldTime = user.lastAccess;
        uint elapsed = newTime - oldTime;
        uint amntToPay = user.dailyPrice * elapsed;
        user.acct.transfer(amntToPay);
        user.lastAccess = newTime;
        
        //With research, it may be possible to use some of Yodlee's other APIs
        //To transfer actual money from our account to their account.
        //Unfortunately it does not seem Blockchain technology is at this level
        //yet, but with the opportunity to pursue this business plan, we would
        //potentially attempt to create our own public blockchain (and most
        //likely accompanying cryptocurrency) in order to develop a more
        //versatile blockchain tech.
    }

    function addFunds() public payable {}

    function () public {
        throw;
    }
}
