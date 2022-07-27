def prepareEtherScanAPIParametersForGetContractABI(key, address):
    return {
        "module": "contract",
        "action": "getabi",
        "address": address,
        "apikey": key
    }
def handleEtherScanAPIResponseForGetContractABI(reponse):
    data = reponse.json()
    contractABI = data['result']
    return contractABI

def prepareBscScanAPIParametersForGetContractABI(key, address):
    return {
        "module": "contract",
        "action": "getabi",
        "address": address,
        "apikey": key
    }
def handleBscScanAPIResponseForGetContractABI(reponse):
    data = reponse.json()
    contractABI = data['result']
    return contractABI