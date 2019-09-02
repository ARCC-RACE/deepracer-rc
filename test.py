import web_interface_core
import time

client = web_interface_core.DRInterface("uGRqirr3", "192.168.1.101")
print(client.log_on())
#print(client.get_models())
#print(client.get_is_usb_connected())
print(client.set_manual_mode())
client.start_car()
print(client.send_drive_command(1, 0.05))
time.sleep(5)
print(client.stop_car())
