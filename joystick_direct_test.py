import argparse
import multiprocessing as mp
import time

import robot_control
from config import load_config, save_config


def main():
    cfg = load_config()
    parser = argparse.ArgumentParser(description="Run one direct joystick controller without GUI.")
    parser.add_argument("robot", choices=["diagnost", "surgeon"])
    parser.add_argument("--joystick", type=int, default=None)
    args = parser.parse_args()

    if args.joystick is not None:
        if args.robot == "surgeon":
            cfg.joystick_master_id = args.joystick
        else:
            cfg.joystick_slave_id = args.joystick
        save_config(cfg)

    host = cfg.surgeon_ip if args.robot == "surgeon" else cfg.diagnost_ip
    is_master = args.robot == "surgeon"

    auto = mp.Value("i", 1)
    lock = mp.Value("i", 0)
    heartbeat = mp.Queue()
    shared_path = [[]]

    print(f"Starting direct joystick control: {args.robot} {host}:{cfg.control_port}")
    print("Move the joystick. Press Ctrl+C to stop.")

    process = mp.Process(
        target=robot_control.main,
        args=(host, is_master, auto, lock, shared_path, heartbeat, cfg.diagnost_ip if is_master else None),
        name=f"{args.robot}_direct_test",
    )
    process.start()
    try:
        while process.is_alive():
            while not heartbeat.empty():
                print("heartbeat:", heartbeat.get())
            time.sleep(0.5)
    except KeyboardInterrupt:
        lock.value = 1
        time.sleep(0.3)
        process.terminate()
    finally:
        process.join(timeout=2)
        if process.is_alive():
            process.kill()


if __name__ == "__main__":
    mp.freeze_support()
    main()
