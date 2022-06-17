## How to launch an attack

1. `mkdir AttackSandbox && cd AttackSandbox`
2. `cp ../ConfigFiles/* .`
4. `mkdir contracts && cp ../BaconProtocol/Exploit.sol contracts/`
5. `mkdir scripts && cp ../BaconProtocol/Attack.ts scripts/`
3. `npm install`
4. `npx hardhat run scripts/Attack.ts`

5. `cd .. && mv AttackSandbox AttackSandbox-BaconProtocol`



