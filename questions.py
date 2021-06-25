CHOICES = {
    'actions_choices': [
        'Download All Templates',
        'Upload All Templates to a Vmanage Device',
        'Download Feature Templates from a VManage Device',
        'Upload Feature Templates to a VManage Device',
        'Download Device Templates from a VManage Device'
    ],
    'template_options': [
        'all'
    ]
}

QUESTIONS = {
    'device_info':  [
        {
            'type': 'input',
            'name': 'address',
            'message': 'Vmanage Address([IP/address] or [IP/address]:port)'
        },
        {
            'type': 'input',
            'name': 'username',
            'message': 'Username'
        },
        {
            'type': 'password',
            'name': 'password',
            'message': 'Vmanage Password'
        },
        {
            'type': 'input',
            'name': 'is_https',
            'message': 'Is HTTPS(y/n)'
        }
    ],
    'save_filename': [
        {
            'type': 'input',
            'name': 'filename',
            'message': 'File Name in which feature templates are to be saved -> '
        }
    ],
    'upload_filename': [
        {
            'type': 'input',
            'name': 'filename',
            'message': 'File to Upload from'
        }
    ],
    'actions_question': [
        {
            'type': 'list',
            'name': 'action_option',
            'message': 'What Action Do You want to take?',
            'choices': CHOICES['actions_choices']
        }
    ],
    'template_questions': [
        {
            'type': 'input',
            'name': 'templates_save_name',
            'message': 'What would you like to save these templates as ?'
        }
    ]

}
