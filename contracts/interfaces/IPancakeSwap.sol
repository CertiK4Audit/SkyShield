pragma solidity ^0.8.0;

interface IPancakeSwap {
    function swap(uint amount0Out, uint amount1Out, address to, bytes calldata data) external;
    function skim(address to) external;
    function sync() external;
}