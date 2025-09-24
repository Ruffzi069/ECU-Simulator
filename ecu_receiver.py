import can, yaml, threading, datetime
from can.interface import Bus

with open('ecu_config.yaml') as f:
    config = yaml.safe_load(f)

print("Reciever Started.......")

receiver = Bus(interface="socketcan", channel="vcan0", bitrate=config["can"]["bitrate"], can_filters=config["filters"], receive_own_messages=True)
logger = Bus(interface="socketcan", channel="vcan0", bitrate=config["can"]["bitrate"], can_filters=config["filters"])

state = None

def log_file_thread():
    with open("ecu_logs.txt", "a") as logfile:
        while True:
            msg = logger.recv(timeout=3.0)
            if msg is None:
                logfile.write('[ARBITRATION_ID: , DATA: , EXTENDED: ]\n')
                logfile.flush()
                continue
            
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            
            data_list = list(msg.data)
            arb_id = hex(msg.arbitration_id)
            logfile_line = (f"[RECEIVER] [{timestamp}] [ARBITRATION_ID: {arb_id} , DATA: {data_list}, EXTENDED: False]\n")

            logfile.write(logfile_line)
            logfile.flush()
log_threading = threading.Thread(target=log_file_thread, daemon=True)
log_threading.start()


try:
    while True:
        msg = receiver.recv(timeout=1.0)
        if msg is None:
            continue
            print("No Messages Now!")

        for name,cmd in config["commands"].items():

            if msg.arbitration_id == cmd["arbitrary_id"]:
                if msg.data == bytearray(cmd["data"]):
                    message = cmd["response"]
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
                    try:
                        if
                        response = cmd["response"].format(doors=cmd["data"][1])
                    except KeyError:
                        response = message
                    print(f'Message : {response}')

except KeyboardInterrupt:
    print("\nKeyboard Interrupted!")

receiver.shutdown()
logger.shutdown()
