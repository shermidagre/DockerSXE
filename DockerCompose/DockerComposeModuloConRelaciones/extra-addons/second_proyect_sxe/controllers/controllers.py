# -*- coding: utf-8 -*-
from odoo import http


class SecondProyectSxe(http.Controller):
    @http.route('/second_proyect_sxe/second_proyect_sxe', auth='public')
    def index(self, **kw):
        return "Hello, world"

    @http.route('/second_proyect_sxe/second_proyect_sxe/objects', auth='public')
    def list(self, **kw):
        return http.request.render('second_proyect_sxe.listing', {
            'root': '/second_proyect_sxe/second_proyect_sxe',
            'objects': http.request.env['second_proyect_sxe.second_proyect_sxe'].search([]),
        })

    @http.route('/second_proyect_sxe/second_proyect_sxe/objects/<model("second_proyect_sxe.second_proyect_sxe"):obj>', auth='public')
    def object(self, obj, **kw):
        return http.request.render('second_proyect_sxe.object', {
            'object': obj
        })

