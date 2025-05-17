# -*- coding: utf-8 -*-
# Part of ERPQuick. See LICENSE file for full copyright and licensing details.

{
    'name': 'ERPQuick School Management',
    'version': '1.0',
    'license': 'LGPL-3',
    'summary': 'School Management System',
    'author': 'ERPQuick',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/student_views.xml',
        'views/teacher_views.xml',
        'views/class_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}