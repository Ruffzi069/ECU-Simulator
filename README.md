# ECU Simulator

Hello guys! This is just a software simulator of how ECU works!
Currently, I have included the 3 Functionalities : `Lock, Unlock, Horn`

Here are the commands to run :
- `pip3 install -r requirements.txt`

---------------------------------------------------------------------------

## Creating a Virtual CAN:
In order to run this simulator, we need to create a virtual can network for the communication between sender and the receiver.
``
sudo modprobe vcan
sudo ip link add dev vcan0 type vcan
sudo ip link set up vcan0
``

- `python3 ecu_sender.py (Tab 1)`
- `python3 ecu_receiver.py (Tab 2)`

