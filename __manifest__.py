# -*- coding: utf-8 -*-
{
    'name': "Real Estate Management",

    'summary': """
        This module handle the Advanced Project""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Quadova",
    'website': "https://quadova.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base','product', 'stock','purchase'],

    # always loaded
    'data': [
        # security
        'security/ir.model.access.csv',
        
        # wizard
        'wizard/pm_purchase_request.xml',
        
        # views
        'views/pm_contract_view.xml',
        'views/pm_project_view.xml',
        'views/pm_term_view.xml',
        'views/pm_sub_term_view.xml',
        'views/pm_purchase_request_view.xml',
        'views/pm_employee_view.xml',
        'views/pm_tool_view.xml',
        'views/pm_contractor_subterm_view.xml',
        'views/pm_contractor_view.xml',

        # seq
        'data/pm_data.xml',
        
        # menu
        'views/pm_menu.xml',
    ],
    # only loaded in demonstration mode
    # 'assets': {
    #     'web.assets_backend': [
    #         'Estate_Management/static/src/js/video_display_widget.js',

    #     ],
    # }
}
