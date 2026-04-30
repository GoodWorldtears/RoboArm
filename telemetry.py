import urx
from config import load_config

rob = urx.Robot(load_config().diagnost_ip)

print(rob.get_realtime_monitor().get_all_data())
