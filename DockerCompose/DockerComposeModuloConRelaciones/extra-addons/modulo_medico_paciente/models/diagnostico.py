from odoo import models, fields

class Diagnostico(models.Model):
    _name = 'hospital.diagnostico'
    _description = 'Diagnóstico'

    medico_id = fields.Many2one('hospital.medico', string="Médico", required=True)
    paciente_id = fields.Many2one('hospital.paciente', string="Paciente", required=True)
    sintoma = fields.Text(related='paciente_id.sintomas', string="Síntomas", readonly=True)
    consulta = fields.Char(related='medico_id.consulta', string="Consulta", readonly=True)