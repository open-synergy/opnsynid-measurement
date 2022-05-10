# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openerp import fields, models


class MeasurementTemplate(models.Model):
    _name = "measurement.template"
    _description = "Measurement Template"

    name = fields.Char(
        string="Measurement Template",
        required=True,
    )
    active = fields.Boolean(
        string="Active",
        default=True,
    )
    item_ids = fields.One2many(
        string="Items",
        comodel_name="measurement.template_item",
        inverse_name="template_id",
    )
    note = fields.Text(
        string="Note",
    )
