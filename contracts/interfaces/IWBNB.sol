pragma solidity ^0.8.0;

interface IWBNB {
    function deposit() external payable;
    function withdraw(uint) external;
    function approve(address, uint) external returns (bool);
    function transfer(address , uint ) external returns (bool);
    function balanceOf(address) external returns(uint256);
}