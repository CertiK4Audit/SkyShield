def prepareBscScanAPIParametersForGetContractABI(key, address):
    return {
        "module": "contract",
        "action": "getabi",
        "address": address,
        "apikey": key
    }
def handleBscScanAPIResponseForGetContractABI(reponse):
    data = reponse.json()
    if data['message'] != 'OK':
        print('Error: '+ data['result'])
        return None
    contractABI = data['result']
    return contractABI