import json
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Device:
    def __init__(self, address: str, username: str, password: str, https: bool):
        self._address = address
        self._username = username
        self._password = password

        if https:
            self._https_string = "https"
        else:
            self._https_string = "http"
        self._dataservice_url = f"{self._https_string}://{self._address}/dataservice"

        token_and_cookie = self.generate_auth_token_and_cookie()
        self._token = token_and_cookie['auth_token']
        self._jsession_id = token_and_cookie['jsession_id']
        self._device_templates = None

    def generate_jsession_cookie(self):
        headers = {'Content-type': 'application/x-www-form-urlencoded; charset=utf-8'}
        data = {
            'j_username': self._username,
            'j_password': self._password
        }
        response = requests.post(
            f"{self._https_string}://{self._address}/j_security_check", data=data, headers=headers, verify=False
        )
        return response.cookies.get('JSESSIONID')

    def generate_auth_token_and_cookie(self):
        jsession_id = self.generate_jsession_cookie()
        token_generate_response = requests.get(
            f"{self._dataservice_url}/client/token",
            headers={
                'Content-Type': 'application/json',
                'Cookie': f'JSESSIONID={jsession_id}'
            },
            verify=False
        )
        auth_token = token_generate_response.content.decode('utf-8')
        return {'jsession_id': jsession_id, 'auth_token': auth_token}

    def fetch_templates(self):
        url = f"{self._dataservice_url}/template/device"
        headers = {
            'Cookie': f'JSESSIONID={self._jsession_id}',
            'X-XSRF-TOKEN': self._token
        }
        fetch_templates_response = requests.get(
            url, headers=headers, verify=False
        )
        if fetch_templates_response.status_code != 200:
            raise ValueError(f"Request returned a {fetch_templates_response.status_code} response")
        return json.loads(fetch_templates_response.content.decode('utf-8'))

    def fetch_feature_templates(self):
        url = f"{self._dataservice_url}/template/feature"
        headers = {
            'Cookie': f'JSESSIONID={self._jsession_id}',
            'X-XSRF-TOKEN': self._token
        }
        response = requests.get(
            url, headers=headers, verify=False
        )
        if response.status_code != 200:
            raise ValueError(f"Request returned a {response.status_code} response")
        return json.loads(response.content.decode('utf-8'))

    def fetch_template_by_id(self, template_id: str):
        url = f"{self._dataservice_url}/template/device/object/{template_id}"
        headers = {
            'Content-Type': 'application/json',
            'Cookie': f'JSESSIONID={self._jsession_id}',
            'X-XSRF-TOKEN': self._token
        }
        fetch_single_template_response = requests.get(
            url, headers=headers, verify=False
        )
        if fetch_single_template_response.status_code != 200:
            raise ValueError(f"Request returned a {fetch_single_template_response.status_code} response")

        return json.loads(fetch_single_template_response.content.decode('utf-8'))

    def upload_feature_template(self, data: dict):
        url = f"{self._dataservice_url}/template/feature"
        headers = {
            'Content-Type': 'application/json',
            'Cookie': f"JSESSIONID={self._jsession_id}",
            'X-XSRF-TOKEN': self._token
        }
        upload_feature_template_response = requests.post(
            url, headers=headers, verify=False, json=data
        )

        if upload_feature_template_response.status_code == 200:
            print(f"\033[92m Template {data['templateName']} uploaded successfully to {self._address} \033[0m")
        else:
            if "already exists" in upload_feature_template_response.content.decode("utf-8"):
                print(f"\033[93m {data['templateName']} already exists in the system \033[0m")

        return json.loads(upload_feature_template_response.content.decode('utf-8'))

    def fetch_device_templates(self):
        url = f"{self._dataservice_url}/template/device"
        headers = {
            'Content-Type': 'application/json',
            'Cookie': f"JSESSIONID={self._jsession_id}",
            "X-XSRF-TOKEN": self._token
        }
        fetch_device_templates_response = requests.get(
            url, headers=headers, verify=False
        )
        if fetch_device_templates_response.status_code != 200:
            raise ValueError(f"Request returned a {fetch_device_templates_response.status_code} response")
        self._device_templates = json.loads(fetch_device_templates_response.content.decode('utf-8'))
        return self._device_templates

    def upload_device_feature_template(self, data):
        url = f"{self._dataservice_url}/template/device/feature"
        headers = {
            'Content-Type': 'application/json',
            'Cookie': f"JSESSIONID={self._jsession_id}",
            "X-XSRF-TOKEN": self._token
        }
        response = requests.post(
            url, headers=headers, verify=False, json=data
        )
        if response.status_code == 200:
            print(f"\033[92m Template {data['templateName']} uploaded successfully to {self._address} \033[0m")
        else:
            if "already exists" in response.content.decode("utf-8"):
                print(f"\033[93m {data['templateName']} already exists on vmanage {self._address} \033[0m")

    def upload_device_cli_template(self, data):
        url = f"{self._dataservice_url}/template/device/cli"
        headers = {
            'Content-Type': 'application/json',
            'Cookie': f"JSESSIONID={self._jsession_id}",
            "X-XSRF-TOKEN": self._token
        }
        response = requests.post(
            url, headers=headers, verify=False, json=data
        )
        if response.status_code != 200:
            raise ValueError(f"Request returned a {response.status_code} status code")

    def upload_all_device_templates(self, device_templates):
        for device_template in device_templates:
            if device_template['configType'] == 'cli':
                pass
            elif device_template['configType'] == 'template':
                self.upload_device_feature_template(device_template)
