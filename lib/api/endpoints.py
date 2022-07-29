
import requests
from lib.api.bscscan import handleBscScanAPIResponseForGetContractABI, prepareBscScanAPIParametersForGetContractABI
from lib.api.etherscan import handleEtherScanAPIResponseForGetContractABI, prepareEtherScanAPIParametersForGetContractABI
from lib.setting import setting

def getContractABI(network, address):
    url = setting.getScanAPIURL(network)
    key = setting.getScanAPIKey(network)
    contractABIJson = None
    if network == "eth":
        url = url+"/api"
        params = prepareEtherScanAPIParametersForGetContractABI(key, address)
        response = requests.get(url = url, params = params)
        contractABIJson = handleEtherScanAPIResponseForGetContractABI(response)
    elif network == "bsc":
        url = url+"/api"
        params = prepareBscScanAPIParametersForGetContractABI(key, address)
        response = requests.get(url = url, params = params)
        contractABIJson = handleBscScanAPIResponseForGetContractABI(response)
    else:
        print("Unsupport Network")
    return contractABIJson