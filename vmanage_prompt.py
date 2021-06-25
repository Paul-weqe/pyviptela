from PyInquirer import prompt, Separator
from vmanage.device import Device
from questions import *
import json
import os
import pathlib


class VmanagePrompts:
    @staticmethod
    def get_vmanage_device_info():
        questions = QUESTIONS['device_info']
        answers = prompt(questions)
        return {
            'address': answers.get('address'),
            'username': answers.get('username'),
            'password': answers.get('password'),
            'is_https': answers.get('is_https').upper() == 'Y'
        }

    @staticmethod
    def download_feature_templates():
        device_info = VmanagePrompts.get_vmanage_device_info()
        device = Device(
            device_info['address'], device_info['username'], device_info['password'], device_info['is_https']
        )
        feature_templates = device.fetch_feature_templates()
        filename_question = QUESTIONS['save_filename']
        answer = prompt(filename_question)
        filename = answer.get('filename')
        file = open(filename, 'w')
        file.write(json.dumps(feature_templates))
        file.close()
        address = device_info['address']
        print(f'Feature templates for {address} have been saved in {filename}')

    @staticmethod
    def download_device_templates():
        device_info = VmanagePrompts.get_vmanage_device_info()
        device = Device(
            device_info['address'], device_info['username'], device_info['password'], device_info['is_https']
        )
        device_templates = device.fetch_device_templates()
        filename_question = QUESTIONS['save_filename']
        answer = prompt(filename_question)
        filename = answer.get('filename')
        file = open(filename, 'w')
        file.write(json.dumps(device_templates))
        file.close()

    @staticmethod
    def upload_device_feature_templates():
        filename_question = QUESTIONS['upload_filename']
        filename_answer = prompt(filename_question)
        filename = filename_answer.get('filename')
        template_data = VmanagePrompts.parse_json_file_data(filename)
        device_info = VmanagePrompts.get_vmanage_device_info()
        device = Device(
            device_info['address'], device_info['username'], device_info['password'], device_info['is_https']
        )
        for template in template_data:
            if template['configType'] == "template":
                device.upload_device_feature_template(template)

    @staticmethod
    def upload_feature_template_to_vmanage_device():
        filename_question = QUESTIONS['upload_filename']
        filename_answer = prompt(filename_question)
        filename = filename_answer.get('filename')
        template_data = VmanagePrompts.parse_json_file_data(filename)
        template_choices = [Separator('=The Feature Templates=')]
        for x in template_data['data']:
            template_name = x['templateName']
            template_choices.append({'name': f"{template_name}"})
        template_choices_question = [
            {
                'type': 'checkbox',
                'name': 'feature_templates',
                'message': 'Choose Templates to be uploaded',
                'choices': template_choices
            },
        ]
        template_choices_answer = prompt(template_choices_question)
        chosen_templates = template_choices_answer.get('feature_templates')
        device_info = VmanagePrompts.get_vmanage_device_info()
        device = Device(
            device_info['address'], device_info['username'], device_info['password'], device_info['is_https']
        )
        for feature_template in template_data['data']:
            for chosen_template in chosen_templates:
                if feature_template['templateName'] == chosen_template:
                    feature_template['templateDefinition'] = json.loads(feature_template['templateDefinition'])
                    device.upload_feature_template(feature_template)
                    print(f"Uploaded {feature_template['templateName']} successfully")

    @staticmethod
    def download_all_templates():
        device_info = VmanagePrompts.get_vmanage_device_info()
        device = Device(
            device_info['address'], device_info['username'], device_info['password'], device_info['is_https']
        )
        dir_path = f"{os.getcwd()}/templates/"
        pathlib.Path(dir_path).mkdir(parents=True, exist_ok=True)
        question = [
            {
                'type': 'input',
                'message': 'What would you like this configs to be saved as',
                'name': 'config_name'
            }
        ]
        answer = prompt(question)
        config_name = answer.get('config_name')
        dir_path = f"{dir_path}/{config_name}"
        pathlib.Path(dir_path).mkdir(parents=True, exist_ok=True)
        feature_templates = device.fetch_feature_templates()
        device_templates = device.fetch_device_templates()
        with open(f"{dir_path}/feature_templates.json", "w") as feature_templates_file:
            feature_templates_file.write(json.dumps(feature_templates))
            feature_templates_file.close()

        with open(f"{dir_path}/device_templates.json", "w") as device_templates_file:
            device_templates_file.write(json.dumps(device_templates))
            device_templates_file.close()

        pathlib.Path(f"{dir_path}/feature_templates/").mkdir(parents=True, exist_ok=True)
        pathlib.Path(f"{dir_path}/feature_templates/").mkdir(parents=True, exist_ok=True)
        pathlib.Path(f"{dir_path}/device_templates/cli/").mkdir(parents=True, exist_ok=True)
        pathlib.Path(f"{dir_path}/device_templates/features/").mkdir(parents=True, exist_ok=True)

        for template in feature_templates['data']:
            template_filename = template['templateId']
            with open(f"{dir_path}/feature_templates/{template_filename}.json", "w") as file:
                file.write(json.dumps(template))
                file.close()

        for template in device_templates['data']:
            template_id = template['templateId']
            template_data = device.fetch_template_by_id(template_id)
            if template["configType"] == "file":
                with open(f"{dir_path}/device_templates/cli/{template_id}.json", "w") as file:
                    file.write(json.dumps(template_data))
                    file.close()
            elif template_data["configType"] == "template":
                with open(f"{dir_path}/device_templates/features/{template_id}.json", "w") as file:
                    file.write(json.dumps(template_data))
                    file.close()

    @staticmethod
    def upload_all_templates_vmanage_device():
        template_config_choices = [Separator("==== CONFIG NAMES ====")]
        template_config_choices += os.listdir(os.getcwd() + "/templates")
        template_config_questions = [
            {
                'type': 'list',
                'name': 'template_config_answer',
                'message': 'Choose the template configs you want uploaded',
                'choices': template_config_choices
            }
        ]
        template_config_answers = prompt(template_config_questions)

        base_path = f"{os.getcwd()}/templates/{template_config_answers.get('template_config_answer')}"
        feature_templates_path = f"{base_path}/feature_templates"
        device_cli_templates_path = f"{base_path}/device_templates/cli"
        device_feature_templates_path = f"{base_path}/device_templates/features"

        device_info = VmanagePrompts.get_vmanage_device_info()
        device = Device(
            device_info['address'], device_info['username'], device_info['password'], device_info['is_https']
        )
        rotate_data = {}

        print("\033[1m -------------------------------- UPLOADING FEATURE TEMPLATES --------------------------------- ")
        for feature_template in os.listdir(feature_templates_path):
            with open(f"{feature_templates_path}/{feature_template}", "r") as file:
                file_content = file.read()
                data = json.loads(file_content)
                data["templateDefinition"] = json.loads(data["templateDefinition"])
                response_data = device.upload_feature_template(data)
                if 'templateId' in response_data:
                    final_template_id = response_data["templateId"]
                    initial_template_id = data["templateId"]
                    rotate_data[initial_template_id] = final_template_id
                file.close()

        print("\033[1m ---------------- UPLOADING FEATURE BASED DEVICE TEMPLATES ----------------------------- \033[0m")
        for device_feature_template in os.listdir(device_feature_templates_path):
            with open(f"{device_feature_templates_path}/{device_feature_template}", "r") as file:
                file_content = file.read()
                for x in rotate_data:
                    file_content = file_content.replace(x, rotate_data[x])
                data = json.loads(file_content)
                device.upload_device_feature_template(data)
                file.close()

    @staticmethod
    def parse_json_file_data(filename: str):
        with open(filename, 'r') as file:
            file_data = json.load(file)
        return file_data


def initial_question():
    choices = CHOICES['actions_choices']
    questions = QUESTIONS['actions_question']
    answers = prompt(questions)
    action = answers.get('action_option')
    if action == choices[0]:
        VmanagePrompts.download_all_templates()
    elif action == choices[1]:
        VmanagePrompts.upload_all_templates_vmanage_device()
    elif action == choices[2]:
        VmanagePrompts.download_feature_templates()
    elif action == choices[3]:
        VmanagePrompts.upload_feature_template_to_vmanage_device()
    elif action == choices[4]:
        VmanagePrompts.download_device_templates()


if __name__ == "__main__":
    initial_question()
