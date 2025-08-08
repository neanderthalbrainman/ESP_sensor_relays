import digitalio
import busio
import board
import time
from circuitpython_nrf24l01.rf24 import RF24, address_repr


CE_PIN = digitalio.DigitalInOut(board.IO4)     # Any GPIO
CSN_PIN = digitalio.DigitalInOut(board.IO5)    # Any GPIO
CE_PIN.direction = digitalio.Direction.OUTPUT
CSN_PIN.direction = digitalio.Direction.OUTPUT

SPI_BUS = busio.SPI(clock=board.IO12, MOSI=board.IO11, MISO=board.IO13)


TX_ADDR=b"2Node"
RX_ADDR=b"1Node"
nrf = RF24(SPI_BUS, CSN_PIN, CE_PIN)

#NRF_messages = [] #not used

def SetupRadio():
    nrf.auto_ack = True
    nrf.channel = 76
    nrf.dynamic_payloads = False
    nrf.payload_length = 32
    nrf.open_tx_pipe(TX_ADDR)
    nrf.open_rx_pipe(1, b'1Node')
    nrf.flush_rx()
    nrf.flush_tx()
    nrf.arc = 3
    nrf.data_rate = 1
    nrf.power = -18
    nrf.pa_level = -12
    nrf.listen = True
    
    
    
def PrintRadioConfig():
    nrf.print_details()
    nrf.print_pipes()
    
def TestCarrier():
    nrf.start_carrier_wave()
    time.sleep(3)
    nrf.stop_carrier_wave()
    
SetupRadio()
#PrintRadioConfig() #for debugging
TestCarrier()
class Pinger:
    count = 0

def PingOut(): #early testing, util function
    msg = b"Ping #%d" % Pinger.count or 0
    try:
        nrf.listen = False
        print("Attempting send...", Pinger.count, "NRF any?", nrf.any()) ##his is dumb and won't work - radio isn't listening
        nrf.send(bytes(msg))
    except BaseException as e:
        print("ERR", e)
    Pinger.count+=1

def SendMsg(msg):
    if (type(msg) is not bytes):
        if (len(msg.encode('utf-8')) <= 32):
            message = msg.encode('utf-8')
    else:
        message = msg
    try:
        nrf.listen = False
        #print(message)
        nrf.send(bytes(message))
    except BaseException as e:
       print("err: ", e)
           
SendMsg("INIT - NRF LINK FROM TRUNK")   ##Send this to the Pi - tests that NRF is working      

