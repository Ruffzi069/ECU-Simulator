import can
import yaml
from can.interface import Bus

with open("ecu_config.yaml") as f:
    config = yaml.safe_load(f)

sender = Bus(interface='socketcan', channel="vcan0", bitrate=config["can"]["bitrate"], can_filters=config["filters"], receive_own_messages=True)
receiver = Bus(interface='socketcan', channel="vcan0", bitrate=config["can"]["bitrate"], can_filters=config["filters"], receive_own_messages=True)

user_input = input("Enter your command: ").lower()
cmd = config["commands"].get(user_input)

if cmd:
    msg = can.Message(arbitration_id=cmd["arbitrary_id"], data=cmd["data"] + [1], is_extended_id=False)
    
    try:
        sender.send(msg)
        print(f'MESSAGE SENT ON {sender.channel}')
#        resp1 = cmd["response"].format(doors=cmd["data"][1])
#        print(resp1)
    except can.CanError:
        print("UNEXPECTED ERRROR")

while True:
    message = receiver.recv(timeout=2.0)
    if message is None:
        break
    if "doors" in cmd["response"]:
        resp = cmd["response"].format(doors=cmd["data"][1])
    else:
        resp = cmd["response"]
    print(resp)
print("NO MSGS NOW")

sender.shutdown()
receiver.shutdown()
