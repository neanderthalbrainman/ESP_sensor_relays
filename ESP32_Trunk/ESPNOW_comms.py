import espnow
import wifi
import time
##ROOT NODE - READS IN MSGS FROM BRANCH NODES
e = espnow.ESPNow()
client_mac = b'\x48\x27\xE2\x1D\x90\x20' ##My only remote node, for now. 
e.peers.append(espnow.Peer(mac=client_mac))

def EspNowRead() -> str: ## Read the queued ESPNOW packet
    packet = e.read()
    msg:str = packet or ""
    return (msg)
