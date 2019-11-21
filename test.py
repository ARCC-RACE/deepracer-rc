import web_interface_core
import time

client = web_interface_core.DRInterface("JJo1qfmc", "192.168.1.100")
client.log_on()
# print(client.get_models())
# print(client.get_is_usb_connected())
print(client.set_manual_mode())
client.start_car()
# print(client.send_drive_command(1, 0.05))
# time.sleep(5)
print(client.stop_car())
# print(client.get_uploaded_models())
print("Uploading model")
print(client.upload_model("/home/michael/Desktop/progressive-5.tar.gz", "progressive-5.tar.gz"))
