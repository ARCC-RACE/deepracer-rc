import web_interface_core
import threading
import argparse
import inputs  # https://inputs.readthedocs.io/en/latest/user/intro.html

steer = 0
drive = 0
done = False


def event_loop():
    """
    This function is called in a loop, and will get the events from the
    controller and send them to the functions we specify in the `event_lut`
    dictionary
    """
    global done, drive, steer
    while not done:
        events = inputs.get_gamepad()
        for event in events:
            if event.code == "ABS_RZ":
                drive = event.state / -256.0
            # print('\t', event.ev_type, event.code, event.state)
            if event.code == "ABS_X":
                steer = (event.state - 128) / 128.0
            if event.code == "ABS_RZ":
                drive = event.state / -256.0
            elif event.code == "ABS_Z":
                drive = event.state / 256.0
            if event.code == "BTN_NORTH":
                done = True


def main():
    """Process all events forever."""
    parser = argparse.ArgumentParser()
    parser.add_argument("ip")
    parser.add_argument("password")
    args = parser.parse_args()
    print("Logging onto " + args.ip + " with password: " + args.password)
    client = web_interface_core.DRInterface(args.password, args.ip)
    client.log_on()
    client.set_manual_mode()
    client.start_car()
    t1 = threading.Thread(target=event_loop, name='t1')
    t1.start()
    global done, drive, steer
    while not done:
        client.send_drive_command(steer, drive)
        print("Steering command: " + str(steer) + " Throttle command: " + str(drive))
    client.stop_car()
    t1.join()


if __name__ == "__main__":
    main()
