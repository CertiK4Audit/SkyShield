pragma solidity ^0.8.0;


interface IERC20 {
    function approve(address spender, uint value) external returns (bool);
    function transfer(address to, uint value) external returns (bool);
    function balanceOf(address account) external view returns (uint256);
    function transferFrom(address from, address to, uint value) external returns (bool);
    function decimals() view external returns (uint8);
    function burn(address account, uint256 amount) external;
}