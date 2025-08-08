#!/usr/bin/env python3
import time
from pyrf24 import RF24, RF24_PA_LOW, RF24_1MBPS
from datetime import datetime
import nrf_db_write

CE_PIN    = 25        # BCM GPIO25 for CE
CS_DEVICE = 0         # SPI device 0 → /dev/spidev0.0
ADDR_RX   = b"2Node"  # ESP32 listens here
ADDR_TX   = b"1Node"  # ESP32 sends here


def TestSend():
    radio.stopListening()   # ensures we’re in TX mode
    for i in range(10):
        print("Radio ready? ", radio.available())
        ok = radio.write(b"HELLO ESP32")  # True = multicast (no ACK wait)
        print(f"Pi → ESP32 packet #{i+1} →", "OK" if ok else "FAIL")
        time.sleep(0.1)

def setup_radio():
    radio = RF24(CE_PIN, CS_DEVICE)
    if not radio.begin():
        raise RuntimeError("nRF24 not found (wiring/SPIDEV perms?)")

    # 1) Core RF settings
    radio.setPALevel(RF24_PA_LOW)   # 0 dBm
    radio.setDataRate(RF24_1MBPS)   # 1 Mbps
    radio.setChannel(76)            # Channel 76
    radio.setAutoAck(True)          # hardware ACKs enabled if you use them

    # 2) Static-32B payload mode
    radio.disableDynamicPayloads()
    radio.setPayloadSize(32)

    # 3) Open pipes *before* any TX/RX mode switches
    radio.openReadingPipe(1, ADDR_RX)
    radio.openWritingPipe(ADDR_TX)

    # 4) Dump register state for sanity
    print("\n--- RADIO CONFIGURATION ---")
    radio.printDetails()
    print("---------------------------\n")

    # 5) TX-only test (fire-and-forget)
    #TestSend()

    radio.flush_tx()        # clear TX FIFO
    # 6) Return to RX mode
    radio.startListening()

    return radio

def ParseTextAndSendToDB(text):
    working = text.split(" ")
    temperature = working[0]
    humidity = working[1]
    location = working[4]
    time = datetime.now()
    #print(temperature, humidity, location, time)
    nrf_db_write.SubmitToDB(temperature, humidity, location, time)

def main():
    radio = setup_radio()
    print(f"🔊 Listening on {ADDR_RX!r} …\n")
    rpd = radio.testRPD()
    print("RPD =", rpd)
    while True:
        radio.startListening()
#        print("rpd ", radio.testRPD())
        #print("Radio available?", radio.available())
        if radio.available():
            raw  = radio.read(32)
            text = bytes(raw).rstrip(b'\x00').decode('utf-8', 'ignore')
            print("▶️ Received:", text)
            ParseTextAndSendToDB(text)
        time.sleep(5)

if __name__ == "__main__":
    main()
