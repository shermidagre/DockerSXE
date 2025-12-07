# -*- coding: utf-8 -*-

from odoo import models, fields, api
import datetime

class second_proyect_sxe(models.Model):

    _inherit = 'res.partner'

    f_nac = fields.Date("Fecha de nacimiento")

    edad = fields.Integer(string = "Edad", readonly = True, compute = "_calcular_edad_china", store = True)
    signo_chino = fields.Char(string = "Signo Chino", readonly = True, compute = "_calcular_chinada", store = True)

    codigo_socio = fields.Char(string="Código de Socio")

    nivel_fidelidad = fields.Selection(
        [
            ('estandar', 'Estándar'),
            ('premium', 'Premium'),
            ('gold', 'Gold')
        ],
        string="Nivel de Fidelidad",
        compute="_compute_nivel_fidelidad",
        store=True,
        default='estandar'
    )

    @api.depends('f_nac')
    def _calcular_edad_china(self):
        for record in self:
            today = datetime.date.today()
            if record.f_nac:
                age = today.year - record.f_nac.year
                record.edad = age
            else:
                record.edad = 0

    @api.depends('f_nac')
    def _calcular_chinada(self):
        for record in self:
            if record.f_nac:
                record.signo_chino = "Calculado"
            else:
                record.signo_chino = "Sin calcular"

    @api.depends('codigo_socio')
    def _compute_nivel_fidelidad(self):
        for record in self:
            if not record.codigo_socio:
                # Si el código está vacío
                record.nivel_fidelidad = 'estandar'
            elif record.codigo_socio.upper().startswith('G'):
                # Si el código empieza por "G"
                record.nivel_fidelidad = 'gold'
            else:
                # Si el código tiene valor y no empieza por "G"
                record.nivel_fidelidad = 'premium'



