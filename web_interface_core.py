import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
from bs4 import BeautifulSoup
import urllib3
import json


# Class that interfaces with thea web page to control the DeepRacer, load models, and receive camera data
class DRInterface():
    def __init__(self, password, ip='192.168.1.100', name="deep_racer"):
        self.session = requests.Session()
        urllib3.disable_warnings()
        self.password = password
        self.name = name
        self.ip = ip
        self.headers = None

        # basic URLs that are needed for logging on and retrieving data
        self.URL = "https://" + self.ip + "/"  # Main URL for logging onto DeepRacer web page for first time
        self.post_login_url = self.URL + "/login"  # Where to redirect with login password
        self.video_url = self.URL + "/route?topic=/video_mjpeg&width=480&height=360"
        self.manual_drive_url = self.URL + "/api/manual_drive"
        self.max_nav_throttle_url = self.URL + "/api/max_nav_throttle"
        self.drive_mode_url = self.URL + "/api/drive_mode"
        self.start_stop_url = self.URL + "/api/start_stop"
        self.home_url = self.URL + "/home"
        self.get_is_usb_connected_url = self.URL + "/api/is_usb_connected"
        self.get_models_url = self.URL + "/api/models"
        self.upload_models_url = self.URL + "/api/uploadModels"
        self.upload_model_list_url = self.URL + "/api/uploaded_model_list"
        self.manual_drive_url = self.URL + "/api/manual_drive"

        # state variables
        self.manual = True
        self.start = False

    def log_on(self):
        # Get the CSRF Token and logon on to a DeepRacer control interface session
        response = self.session.get(self.URL, verify=False, timeout=10)  # Cannot verify with Deep Racer
        soup = BeautifulSoup(response.text, 'lxml')
        csrf_token = soup.select_one('meta[name="csrf-token"]')['content']
        # primary header to login and get is_usb_connected
        self.headers = {'X-CSRFToken': csrf_token,
                        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"}
        payload = {'password': self.password}
        post = self.session.post(self.post_login_url, data=payload, headers=self.headers, verify=False)
        # secondary header for other commands
        self.headers = {'X-CSRFToken': csrf_token,
                        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36",
                        "referer": self.URL + "/home",
                        "origin": self.URL,
                        "accept-encoding": "gzip, deflate, br",
                        "content-type": "application/json;charset=UTF-8",
                        "accept": "*/*",
                        "sec-fetch-mode": "cors",
                        "sec-fetch-site": "same-origin",
                        "accept-language": "en-US,en;q=0.9",
                        "x-requested-with": "XMLHttpRequest"
                        }
        return json.loads(post.text)

    '''General purpose functions for interacting with the DeepRacer'''

    def get_home(self):
        # Send a get request to the home page (required after login)
        get = self.session.get(self.home_url, headers=self.headers, verify=False)
        self.session.get(self.URL + "/static/bundle.css", headers=self.headers, verify=False)
        self.session.get(self.URL + "/static/react@16.production.min.js", headers=self.headers, verify=False)
        self.session.get(self.URL + "/static/react-dom@16.production.min.js", headers=self.headers, verify=False)
        self.session.get("https://code.jquery.com/pep/0.4.3/pep.js", headers=self.headers, verify=False)
        self.session.get(self.URL + "/static/bundle.js", headers=self.headers, verify=False)
        return get

    def get_is_usb_connected(self):
        return json.loads(self.session.get(self.get_is_usb_connected_url, headers=self.headers, verify=False).text)

    def send_drive_command(self, steering_angle, throttle):
        # Set angle and throttle commands from -1 to 1
        data = {'angle': steering_angle, 'throttle': throttle}
        return json.loads(self.session.put(self.manual_drive_url, json=data, headers=self.headers, verify=False).text)

    def set_manual_mode(self):
        # Set the car to take in input from manual channels (ie this program)
        self.stop_car()
        data = {'drive_mode': "manual"}
        return json.loads(self.session.put(self.drive_mode_url, json=data, headers=self.headers, verify=False).text)

    def stop_car(self):
        data = {'start_stop': "stop"}
        return json.loads(self.session.put(self.start_stop_url, json=data, headers=self.headers, verify=False).text)

    def start_car(self):
        data = {'start_stop': "start"}
        return json.loads(self.session.put(self.start_stop_url, json=data, headers=self.headers, verify=False).text)

    def get_raw_video_stream(self):
        # Get the video stream
        return json.loads(self.session.get(self.video_url, stream=True, verify=False).text)

    '''Functions for running autonomous mode'''

    def get_models(self):
        return json.loads(self.session.get(self.get_models_url, headers=self.headers, verify=False).text)

    def get_uploaded_models(self):
        return json.loads(self.session.get(self.upload_model_list_url, headers=self.headers, verify=False).text)

    def set_autonomous_mode(self):
        # Set the car to use the autonomous mode and not care about input from this program
        self.stop_car()
        data = {'drive_mode': "auto"}
        return json.loads(self.session.put(self.drive_mode_url, json=data, headers=self.headers, verify=False).text)

    def set_throttle_percent(self, throttle_percent):
        # Set the percent throttle from 0-100% (note for manual mode this has no effect)
        data = {'throttle': throttle_percent}
        return json.loads(
            self.session.put(self.max_nav_throttle_url, json=data, headers=self.headers, verify=False).text)

    def load_model(self, model_name):
        model_url = self.URL + "/api/models/" + model_name + "/model"
        return json.loads(self.session.put(model_url, headers=self.headers, verify=False).text)

    def manual_drive(self):
        data = {"angle": 0, "throttle": 0}
        return json.loads(self.session.put(self.manual_drive_url, json=data, headers=self.headers, verify=False).text)

    def upload_model(self, model_zip_path, model_name):
        model_file = open(model_zip_path, 'rb')
        headers = self.headers
        multipart_data = MultipartEncoder(
            fields={
                # a file upload field
                'file': (model_name, model_file, None)
            }
        )
        headers['content-type'] = multipart_data.content_type
        return json.loads(self.session.put(self.upload_models_url, data=multipart_data, headers=headers, verify=False).text)
