# -*- coding: utf-8 -*-
# Part of ERPQuick. See LICENSE file for full copyright and licensing details.

{
    'name': 'ERPQuick School Management',
    'version': '1.0',
    'license': 'LGPL-3',
    'summary': 'School Management System',
    'author': 'ERPQuick',
    'depends': ['board', 'web', 'website', 'hr', 'contacts'],
    'data': [
        'security/ir.model.access.csv',
        'views/res_company_views.xml',
        'views/res_users_views.xml',
        'views/res_partner_views.xml',
        'views/student_views.xml',
        'views/teacher_views.xml',
        'views/class_views.xml',
        'views/academic_year_views.xml',
        'views/academic_term_views.xml',
        'views/menu_views.xml',

        'data/ir_sequence.xml',
        'data/category_data.xml',
        'data/res_partner_data.xml',
    ],
    'images': ['static/description/icon.png'],
    'installable': True,
    'auto_install': False,
    'application': True,
}