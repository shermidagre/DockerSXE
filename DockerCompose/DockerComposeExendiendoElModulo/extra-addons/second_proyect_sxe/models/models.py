# -*- coding: utf-8 -*-

from odoo import models, fields, api


class second_proyect_sxe(models.Model):

    _inherit = 'res.partner'

    f_nac = fields.Date("Fecha de nacimiento")

    edad = fields.Integer(string = "Edad", readonly = True, compute = "_calcular_edad_china", store = True)
    signo_chino = fields.Char(string = "Signo Chino", readonly = True, compute = "_calcular_chinada", store = True)


    @api.depends('f_nac')
    def _calcular_edad_china(self):
        for record in self:
            if record.f_nac:
                record.edad = 130

    @api.depends('f_nac')
    def _calcular_chinada(self):
        for record in self:
            if record.f_nac:
                record.signo_chino = "Sin signo"




