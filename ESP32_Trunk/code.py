##This should be written to the trunking ESP32 node, to relay via NRF to the Raspi. 
# code.py runs on boot. 
import time
import board
import espnow
from circuitpython_nrf24l01.rf24 import * 
import nrf24_comms
import ESPNOW_comms

#
#C = 48:27:E2:1D:90:10 <---- THIS
#B = 48:27:E2:1D:90:20 <---- REMOTE

##This is an ESP32 relay node.
##This node is the HEAD and sends data via NRF to my pi.
## Step 1 -- Connect to remote nodes via ESPNOW ---
## Step 2 -- Connect to Pi using NRF module
## Step 3 -- Ingest data from ESPNOW and forward to NRF

mylocation = "TRUNK"

def PrintMyMAC():
    mac = wifi.radio.mac_address
    print("This device MAC:", ":".join([f"{b:02X}" for b in mac]), "Device is ", mylocation)


#esp_comms = nrf24_comms.NRF_messages

while True:
    #nrf24_comms.PingOut()
    out = ESPNOW_comms.EspNowRead()
    if isinstance(out, espnow.ESPNowPacket):
        #out.msg
        nrf24_comms.SendMsg(out.msg)
    else:
        print("No valid packet")
    time.sleep(1)


