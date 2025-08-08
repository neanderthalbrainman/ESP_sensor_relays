# ESP_sensor_relays
Personal/Education: 
This project is designed to relay sensor data from ESP32(s) to a mySQL database living on a Raspi. 

The configuration is: 

(Branch)          (Trunk)
ESP32+sensor(s) -> ESP32 -> Raspi/MySQL

The ESP32s use CircuitPython. 
The Truck ESP32 utilizes the CircuitPython nrf lib.
The Pi is using PyPi for SPI comms with the nrf module. 
