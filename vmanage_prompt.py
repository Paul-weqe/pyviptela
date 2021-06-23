from PyInquirer import prompt, Separator
from vmanage.device import Device
from questions import *
import json


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
        file.write(feature_templates)
        file.close()
        address = device_info['address']
        print(f'Feature templates for {address} have been saved in {filename}')

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
        VmanagePrompts.download_feature_templates()
    elif action == choices[1]:
        VmanagePrompts.upload_feature_template_to_vmanage_device()


if __name__ == "__main__":
    initial_question()
