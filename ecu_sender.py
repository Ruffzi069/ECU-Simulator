import can, yaml, datetime, threading
from can.interface import Bus

with open('ecu_config.yaml') as f:
    config = yaml.safe_load(f)


sender = Bus(interface="socketcan", channel="vcan0", bitrate=config["can"]["bitrate"], can_filters=config["filters"], receive_own_messages=True)
logger = Bus(interface="socketcan", channel="vcan0", bitrate=config["can"]["bitrate"], can_filters=config["filters"])

state = 1

def log_file_thread():
    with open("ecu_logs.txt", "a") as logfile:
        while True:
            msg = logger.recv(timeout=1.0)
            if msg is None:
                logfile.write('[ARBITRATION_ID: , DATA: , EXTENDED: ]\n')
                logfile.flush()
                continue
            
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            data_list = list(msg.data)
            arb_id = hex(msg.arbitration_id)
            logfile_line = (f"[SENDER] [{timestamp}] [ARBITRATION_ID: {arb_id} , DATA: {data_list} , EXTENDED: False]\n")

            logfile.write(logfile_line)
            logfile.flush()
log_threading = threading.Thread(target=log_file_thread, daemon=True)
log_threading.start()


try :
    while True:

        user_input = input("Enter the command: ").lower()
        cmd = config["commands"].get(user_input)        
        if state == 1 and user_input in "lock":
            print("Already Locked")
        elif state == 1 and user_input in "unlock":
            state = 0
            cmd["data"][2] = state
            msg = can.Message(arbitration_id=cmd["arbitrary_id"], data=cmd["data"], is_extended_id=False)
            sender.send(msg)
        elif state == 0 and user_input in "lock":
            state = 1
            cmd["data"][2] = state
            msg = can.Message(arbitration_id=cmd["arbitrary_id"], data=cmd["data"], is_extended_id=False)
            sender.send(msg)
        else:
            print("Already Unlocked")
             
except KeyboardInterrupt:
    print("\n Keyboard Interrupted!")


finally:
    sender.shutdown()
    logger.shutdown()
