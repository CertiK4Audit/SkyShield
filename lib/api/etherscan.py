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