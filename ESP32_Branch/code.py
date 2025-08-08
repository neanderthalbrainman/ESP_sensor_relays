##Written for the ESP32 N2R8 WROOM1 with NeoPixel built in. 

import espnow
import wifi
import time
import adafruit_dht
import board
import neopixel

neoPin = board.NEOPIXEL
neoPixels = 1

pixels = neopixel.NeoPixel(neoPin, neoPixels, brightness=0.1, auto_write=True)
pixels.show()

dhtDevice = adafruit_dht.DHT11(board.IO15)

myLocation = "Remote - Shed"

#REMOTE (sends to Trunk) 
#B: 48:27:E2:1D:90:20 <--- THIS
#C: 48:27:E2:1D:90:10 <--- OTHER

mac_bytes = wifi.radio.mac_address  # returns bytes like b'\xaa\xbb\xcc\xdd\xee\xff'
mac_str = ":".join([f"{b:02X}" for b in mac_bytes])


client_mac = b'\x48\x27\xE2\x1D\x90\x10'
print("Wi-Fi MAC (ESPNOW):", mac_str)

e = espnow.ESPNow()

def RegisterPeer(mac):
    macstr = mac.split(":")
    print(macstr[0])
    bytemac = bytes([int(part, 16) for part in macstr])
    print(len(bytemac))
    e.peers.append(espnow.Peer(mac=bytemac))


def NeoPixelErrorFlash():
    RED = (255, 0, 0, 0)
    pixels.brightness = 0.1
    pixels.fill(RED)
    pixels.show()

def NeoPixelSendStart():
    BLUE = (0, 0, 255, 0)
    pixels.brightness = 0.1
    pixels.fill(BLUE)
    pixels.show()

def NeoPixelSendOk():
    GREEN = (0, 255, 0, 0)
    pixels.brightness = 0.1
    pixels.fill(GREEN)
    pixels.show()

def NeoPixelSendIdle():
    YELLOW = (255, 255, 0, 0)
    pixels.fill(YELLOW)
    pixels.brightness = 0.02
    pixels.show()


RegisterPeer("48:27:E2:1D:90:10")
while True:
    if (len(e.peers) == 0):
        print("ERROR, no peers")
        NeoPixelErrorFlash()
        break
    # Send something
    
    temperature_c = dhtDevice.temperature
    humidity = dhtDevice.humidity
    
    print(
        "Temp: {:.1f} C    Humidity: {}% ".format(
            temperature_c, humidity
        )
    )
    
    NeoPixelSendStart()
    e.send(str(temperature_c) + " " + str(humidity) + " " + myLocation)
    NeoPixelSendOk()
    # Listen for incoming message (non-blocking) #not currently used - planned for control commands
    msg = e.read()
    if msg:
        peer_mac, data = msg
        print("Received from "+ peer_mac.hex(':') + ": " + data)
    NeoPixelSendIdle()
    time.sleep(1)
