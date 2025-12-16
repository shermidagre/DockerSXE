# -*- coding: utf-8 -*-
# from odoo import http


# class ModuloMedicoPaciente(http.Controller):
#     @http.route('/modulo_medico_paciente/modulo_medico_paciente', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/modulo_medico_paciente/modulo_medico_paciente/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('modulo_medico_paciente.listing', {
#             'root': '/modulo_medico_paciente/modulo_medico_paciente',
#             'objects': http.request.env['modulo_medico_paciente.modulo_medico_paciente'].search([]),
#         })

#     @http.route('/modulo_medico_paciente/modulo_medico_paciente/objects/<model("modulo_medico_paciente.modulo_medico_paciente"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('modulo_medico_paciente.object', {
#             'object': obj
#         })

