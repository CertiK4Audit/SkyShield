## How to use this tool

### Environments
1. Clone the repo or use gitpod to open it
2. In the repo, use `ExploitFramewrok-light` branch
3. If you already installed python3 and pip3, go to step 4 directly.
	3.a. Install python3 (To be complete)
4. Install python dependencies `pip3 install -r requirement.txt`

### Use the framework
1. Run framwork by `python3 framwork.py`
2. See all the PoC template provided by using `list` command
3. Load the PoC template by `load public_burn`
4. Update settings by using commands specified in the next section
5. Run the exploit by using `test`

## Command Table



## Functional Requirements
### Basic Requirements
1. Developers or auditors only need to care about the scripts and contracts for POC,  instead of setup environment and network.
2. Developers or auditors can share their POCs,  test and modify others' POCs easily.
3. Developers or auditors can setup their POCs with initialized parameters under particular network and block number. 
4. Developers can easily get a startup template to begin their development of POCs
5. Some convenient tools can help auditor develop their POC more efficiently
### Tools Requirements
#### Search 
1. Developers can search interfaces for common used decentralized exchange platform and lending platform
2. Developers can get the interface of specific address, if the contract is verified
3. Developers can search the address of common used token
4. Developers can search the address of common used router of particular platform
#### Query
1. Developer can query a specific function in specific verified address at particular blockNumber
2. Developer can query a specific function in specific unverified address at particular blockNumber with imported interface solidity file or ABI json file
#### Flatten
1. Developer can flatten the source code to generate interface to help organize and collect frequently used interface   
### Advanced Requirements
## Directory Layout
1. `configurations`
	- configurations file for hardhat, node.js and typescirpt environment
		- `hardhat.config.ts`
		- `package.json`
		- `tsconfig.json`
2. `lib`
	- `api`: Handle the API call to different networks
	- `tools`
		- `search`: Source code for `search` command
		- `query`: Source code for `query` command
		- `flatten`: Source code for `flatten` command 
	- `command.py`: Source code for handle each command  
	- `exploit.py`:  A global variable. It's a class for specific exploit, for getting the information of specific exploit and modifying the `config.yml` of specific exploit
	- `setting.py`: A global variable. It's a class for getting the URL, Private key and the path to particular directories from `setting.yml`
	- `util.py`: Some utilities for searching files, copying files and preparing hardhat  
3. `framework.py`: The entrance of framework
4. `setting.yml`: The setting file to save the URL for node of different network, the URL for different Scan API, the URL for Github repositories, corresponded private key for API, path to particular directory.
5. `exploits`: This directory is used to save POC
6. `POC_Template`: This directory is used to save the downloaded content from  https://github.com/CertiK-Yuannan/PoC_Template.git
## Usage
### Run Framework
1. Prerequisite
	- Python 3.x
	- Node.js 16
2. Installation
	-  Clone project: `git clone https://github.com/CertiK-Yuannan/SkyShield.git`
	- Switch to the branch `ExploitFramework-light`: `git checkout ExploitFramework-light`
3. Install requirements.txt: `pip3 install -r requirements.txt`
4. Run the framework: `python3 framework.py`
### Basic Command
1. Show all commands: `help`
2. Exit framework: `exit`
3. Clear command shell: `clear`
4. Show the info of specific command: `help [commmand]`
### Develop and Test POC
1. **Initialize the framework**
	- Command: `init`
	- This command will prepare the environment for hardhat, installing all required node packages, which will be saved in `configurations/node_modules`. Also, it will download the frequently used interfaces and some databases for tokens, DEX platform, and lending platform from https://github.com/CertiK-Yuannan/PoC_Template.git
2. **List all POCs**
	- Command: `list`
	- Sources
		- Local: Under the folder `exploits`. The name of exploit is the folder name under `exploits`
		- Github: https://github.com/CertiK-Yuannan/PoC_Template.git
3. **Load a POC**
	- Command: `load [POC_name]`
	- This command will firstly search the POC in local `exploits` folder. If existed, it will load the `config.yml` of this POC. If not existed, it will try to download the POC from Github repo and save it to `exploits` folder. If still not existed, this POC is not found.
4. **The basic structure of a POC**
	- `attack.ts`: A TypeScript script to initialize the parameters, addresses of POC, deploy `exploit.sol` contract, execute exploit, call function and check the results. It will be executed by HardHat.  
		- **The basic structure of `attack.ts`**
	```typescript
	// Import needed interface factories, which will be generated automatically according to the exploit.sol and interfaces file 
	import {Exploit__factory, IERC20__factory} from "../typechain";
	import hre, { ethers } from "hardhat"	
	import YAML from 'yaml'	
	import fs from 'fs'

	async function main() {
	// Read parameters from config.yml
	const config_file = fs.readFileSync('config.yml', 'utf8');
	const config = YAML.parse(config_file);
	console.log(config.address.PAIR);
	
	// Prepare the account
	const [signer] = await hre.ethers.getSigners();
	
	// Deploy exploit contract with intialized parameters from config.yml
	const exploit = await new Exploit__factory(signer).deploy(
	config.address.PAIR,
	config.address.ROUTER,
	config.address.VULNERABLE_TOKEN,
	config.address.WBNB);
	
	console.log("Exploit contract deployed to: ",exploit.address)
	const WBNB = IERC20__factory.connect(config.address.WBNB,signer);
	console.log("Attacker WBNB balance:", hre.ethers.utils.formatUnits(await WBNB.balanceOf(signer.address),await WBNB.decimals()))

	// Execute exploit contract
	const exploitTx = await exploit.attack({value: ethers.utils.parseEther("500")});
	console.log("Exploiting... transcation: ",exploitTx.hash)
	await exploitTx.wait()
	console.log("Exploit complete.")
	
	// Display result
	console.log("Attacker WBNB balance:",hre.ethers.utils.formatUnits(await WBNB.balanceOf(signer.address),await WBNB.decimals()))
	}
	
	main().catch((error) => {
	console.error(error);
	process.exitCode = 1;
	});
	```
	- `exploit.sol`: The smart contract for POC
	- `config.yml`:  The configuration file for POC
		- **The structure of `config.yml`**
	```yml
	# The description and helper of this exploit
	description: "On Jan-17-2022 03:34:17 AM +UTC, an attacker manipulate the price of BURG in the PancakeSwap and gained ~77K worth of asset. The attack was caused by a smart contract vulnerability that allows the token to burn in any account."
	# The interfaces required exploit this exploit, these interfaces can be found in this Github repo (https://github.com/CertiK-Yuannan/PoC_Template.git)
	interfaces:
	- PancakeSwap/IERC20.sol
	- PancakeSwap/IPancakeRouter01.sol
	- PancakeSwap/IPancakeRouter02.sol
	- PancakeSwap/IPancakePair.sol
	- PancakeSwap/IWETH.sol
	# The addresses requird by this exploit
	address:
        PAIR: '0x02b0551B656509754285eeC81eE894338E14C5DD'
        VULNERABLE_TOKEN: '0xF40d33DE6737367A1cCB0cE6a056698D993A17E1'
        ROUTER: '0x10ED43C718714eb63d5aA57B78B54704E256024E'
        WBNB: '0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c'
	# Other parameters for this exploit
	parameters:
        amount: '100e18'
        iterations: '5'
	# The URL and blockNumber of archive node or URL to local ganache server 
	networks:
        url: "https://speedy-nodes-nyc.moralis.io/TOKEN/bsc/mainnet/archive"
        blockNumber: '14433982'
        # The url of JSON-RPC (Work in progress)
        JSONRPC: "http://127.0.0.1:8545"
	```
5. **Modify a POC**
	- You can directly change the content of `config.yml`, `attack.ts` and `exploit.sol`
	- Also, you use the command to set particular parameter of `config.yml`
		- Command: `set [Category] [Element] [Value]`
			- Examples: 
				- `set address PAIR 0x02b0551B656509754285eeC81eE894338E14C5DD`
				- `set parameters amount 100`
				- `set networks url https://speedy-nodes-nyc.moralis.io/TOKEN/bsc/mainnet`
				- `set networks blockNumber 14433982`
	- Set the network information via command
		- Command:  `use [Network] [BlockNumber]`
			- Examples:
				- `user bsc`: Without block number
				- `use bsc 14433982`: With block number
				- `use eth`
		- This command will directly copy the URL in `setting.yml` to `config.yml` and also optional set the `blockNumber` in `config.yml`
6. **Testing a POC**
	- Command: `test`
	- This command will attempt to test and run this POC
	- Internal procedures:
		- Create a temporary folder for the environment for HardHat
		- Create required directories
		- Copy related configuration files
		- Create a soft link to `node_modules`
		- Copy `attack.ts`, `exploit.sol` and `config.yml` to temporary folder
		- Copy the related interfaces requested by  `config.yml`
		- Execute `npx hardhat run scripts/attack.ts` to test this POC
		- Display the result
		- Delete temporary folder
### Search
1. **Search contracts' address for common used tokens**
	 - Command: `search address token [Network] [Keyword]`
		 - Examples:
			 - `search address token eth weth`
			 - `search address token bsc wbnb`
			 - `search address token bsc usdt`
2. **Search interfaces**
	- Commands:
		- `search interface global [Keyword]`: **Search the interfaces globally based on keyword from** https://github.com/CertiK-Yuannan/PoC_Template.git
			- Examples:
				- `search interface global weth`
				- `search interface global erc20`
		- `search interface project [Project_Keyword] [Keyword]`: **Search the interfaces based on project and keyword from** https://github.com/CertiK-Yuannan/PoC_Template.git
			- Examples:
				- `search interface project pancake router`
				- `search interface project aave lending`
		- `search interface address [Network] [Address]`: **Get the interface for verified contracts' address via the Scan API (EtherScan, BscScan)**
			- Examples:
				- `search interface address bsc 0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c`
				- `search interface address eth 0x011a014d5e8Eb4771E575bB1000318D509230Afa`
			- If user loaded any exploit, the interface will be saved in the folder of loaded exploit. Otherwise, it will be directly displayed in the terminal 
			- Internal procedures:
				- Attempt to use API to download the ABI file of this address
				- Convert ABI file to interface
### Query
1. **Developer can query a specific function in specific verified address at particular blockNumber**
	- Command: `query [network] [blockNumber] [address] [functionWithParameters]`
		- Examples:
			- `query bsc 19980613 0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c balanceOf(‘0xab69c56d927292197527e3F7Bb0073386636635f’)`
			- `query bsc 19980613 0xEB8d08030017BD1362a5414112CaCb094FA20cE1 getReserves()`
	- Internal procedures
		- Create a temporary folder for environment for Hardhat
		- Copy related configuration files
		- Attempt to use API to download the ABI file of this address, and copy to temporary folder
		- Copy the script `query.ts` to execute function
		- Execute script `npx hardhat run scripts/query.ts`
		- Display the result
		- Delete temporary folder
### Flatten
1. **Developer can flatten the source code to generate interface to help organize and collect frequently used interface (Support `@Openzeppelin`)**
	- Command: `flatten [Path_To_Source_Code] [Relative_Path_To_Interface_Folder_Or_Single_Interface_File] [Output_Directory]`
		- Examples:
			- `flatten /Users/shayyang/Desktop/BlockChain/DEFI Source Code/v3-periphery/contracts/ /interfaces/external/IWETH9.sol /Users/shayyang/Desktop/UniswapV3`
			- `flatten /Users/shayyang/Desktop/BlockChain/DEFI Source Code/v3-periphery/contracts/ /interfaces /Users/shayyang/Desktop/UniswapV3`
	- Internel Procedures
		- Create a temporary folder for environment for Hardhat
		- Copy related configuration files
		- Copy the source code to temporary folder
		- Execute `npx hardhat flatten [path]` for each interface
		- Copy generated interfaces to output directory
## TODO List
### Refine Prerequisite
1. Refine the part of Prerequisite of README.md
2. Update the requirements.txt
3. Update to support node.js 18
### Refine the interactive command
1. Find a better library for building interactive CLI tools
2. Add color to highlight keyword in output message
	- search token
	- search interface
	- flatten
	- query
2. Refine the error message
3. Refine the helpers and tips for each command
### Refine the POC
1. lower the case of `Attack.ts` and `Exploit.ts`
### Support More Network
### Search
1. Support searching the router of frequently used decentralized exchange platform and lending platform
2. Change `search interfaces` to `search interface`
3. Refine the error message of unverified interface
### Query
1. Support `query [network] [blockNumber] [address] [functionWithParameters] interface [path_to_interface]`
2. Support `query [network] [blockNumber] [address] [functionWithParameters] abi [path_to_abi]`
### Flatten
1. Fix the error of multiple SPDX license: https://github.com/NomicFoundation/truffle-flattener/issues/55
