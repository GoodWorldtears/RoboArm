from dataclasses import asdict, dataclass
import json
from pathlib import Path
from typing import Optional


CONFIG_FILE = Path(__file__).with_name("robot_config.json")


@dataclass
class AppConfig:
    diagnost_ip: str = "192.168.8.3"
    surgeon_ip: str = "192.168.8.4"
    diagnost_camera_url: str = "http://192.168.8.150:8081/"
    surgeon_camera_url: str = "http://192.168.8.149:8081/"
    laser_host: str = "192.168.8.149"
    laser_port: int = 9093
    dashboard_port: int = 29999
    joystick_master_id: int = 0
    joystick_slave_id: int = 1
    deadzone: float = 0.2
    linear_velocity: float = 0.015
    diagnost_linear_velocity: float = 0.01
    rotational_velocity: float = 0.19
    acceleration: float = 0.1


def load_config() -> AppConfig:
    if not CONFIG_FILE.exists():
        save_config(AppConfig())
        return AppConfig()

    try:
        with CONFIG_FILE.open("r", encoding="utf-8") as file:
            raw = json.load(file)
    except (OSError, json.JSONDecodeError):
        return AppConfig()

    defaults = asdict(AppConfig())
    defaults.update({key: value for key, value in raw.items() if key in defaults})
    return AppConfig(**defaults)


def save_config(config: AppConfig) -> None:
    with CONFIG_FILE.open("w", encoding="utf-8") as file:
        json.dump(asdict(config), file, indent=2, ensure_ascii=False)


def dashboard_command(host: str, command: str, port: Optional[int] = None, timeout: float = 5.0) -> None:
    cfg = load_config()
    dashboard_port = cfg.dashboard_port if port is None else port
    with __import__("socket").create_connection((host, dashboard_port), timeout=timeout) as sock:
        sock.sendall(f"{command}\n".encode("utf-8"))
