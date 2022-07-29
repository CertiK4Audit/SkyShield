import hre, { ethers } from "hardhat"
import fs from "fs"
import YAML from "yaml"

//TODO Figureout how to query proxy stats?
async function main() {
    const [signer] = await hre.ethers.getSigners();

    const yaml_config_file = fs.readFileSync('config.yml', 'utf8');
    const yaml_config = YAML.parse(yaml_config_file);

    // Read ABI file
    const abi = JSON.parse(fs.readFileSync(yaml_config.path_to_abi, 'utf8'));
    
    // Get address
    const contractAddress = String(yaml_config.address);
    const contractInstance = await hre.ethers.getContractAt(abi, contractAddress);
    console.log("Interacting with contract: ", contractInstance.address);

    // Call function
    console.log("Calling: ", yaml_config.function + "..." )
    const result = await eval("contractInstance." + yaml_config.function);

    // Show result
    console.log(result)
  }
  
  // We recommend this pattern to be able to use async/await everywhere
  // and properly handle errors.
  main().catch((error) => {
    console.error(error);
    process.exitCode = 1;
  });