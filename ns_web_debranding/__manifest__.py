{
    'name': "Backend debranding",
    'version': '12.0.1.0.30',
    'author': 'NinasSofts',
    'license': 'LGPL-3',
    'category': 'Debranding',
    'images': ['images/web_debranding.png'],
    'website': 'https://www.dzitechnology.com',
    'price': 13.99,
    'currency': 'EUR',
    'depends': [
        'web',
        'im_livechat',
        'mail',
    ],
    'data': [
        'data.xml',
        'views.xml',
        'js.xml',
        'pre_install.xml',
    ],
    'qweb': [
        'static/src/xml/web.xml',
    ],
    "post_load": 'post_load',
    'auto_install': False,
    'uninstall_hook': 'uninstall_hook',
    'installable': True,
}
