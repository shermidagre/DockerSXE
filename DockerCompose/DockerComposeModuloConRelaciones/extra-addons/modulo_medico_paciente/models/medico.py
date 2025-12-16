from odoo import models, fields

class Medico(models.Model):
    _name = 'hospital.medico'
    _description = 'Médico'

    id_medico = fields.Char(string="ID Médico", required=True)
    nombre = fields.Char(string="Nombre", required=True)
    apellidos = fields.Char(string="Apellidos", required=True)
    num_colegiado = fields.Char(string="Nº Colegiado", required=True)
    consulta = fields.Char(string="Consulta", required=True)
    diagnostico_ids = fields.One2many('hospital.diagnostico', 'medico_id', string="Diagnósticos")
    paciente_ids = fields.Many2many('hospital.paciente', compute='_compute_pacientes', string="Pacientes atendidos")

    def _compute_pacientes(self):
        for medico in self:
            medico.paciente_ids = medico.diagnostico_ids.mapped('paciente_id')