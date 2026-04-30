# CB-series: https://www.universal-robots.com/how-tos-and-faqs/how-to/ur-how-tos/dashboard-server-port-29999-15690/
# E-series:  https://www.universal-robots.com/how-tos-and-faqs/how-to/ur-how-tos/dashboard-server-e-series-port-29999-42728/
import socket
from config import load_config, dashboard_command

def main(host=None):
    cfg = load_config()
    dashboard_command(host or cfg.surgeon_ip, "unlock protective stop", cfg.dashboard_port)

if __name__ == "__main__":
    main()
