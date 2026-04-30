import urx
from time import sleep
from config import load_config


if __name__ == "__main__":
    rob = urx.Robot(load_config().diagnost_ip, use_rt=True)
    try:
        while True:
            rob.translate_tool([0, 0, -0.05])
            print(rob.getj())
            sleep(1)
            rob.translate_tool([0,0,0.05])

    except(urx.RobotException, TimeoutError, ConnectionError):
        print("--------ERROR--------")
        rob.close()
        print("Connection closed")
