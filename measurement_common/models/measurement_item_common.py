# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class MeasurementItemCommon(models.AbstractModel):
    _name = "measurement.item_common"
    _description = "Abstract Model for Measurement Item"

    @api.multi
    def _compute_allowed_qualitative_option_ids(self):
        obj_option = self.env["measurement.item_type_qualitative_option"]
        for document in self:
            result = []
            if document.item_type_id:
                criteria = [
                    ("type_id", "=", document.item_type_id.id),
                ]
                result = obj_option.search(criteria).ids
            document.allowed_qualitative_option_ids = result

    measurement_id = fields.Many2one(
        string="# Measurement",
        comodel_name="measurement.common",
        required=True,
    )
    item_type_id = fields.Many2one(
        string="Item",
        comodel_name="measurement.item_type",
        required=True,
    )
    sequence = fields.Integer(
        string="Sequence",
        default=5,
        required=True,
    )
    question_type = fields.Selection(
        string="Type",
        selection=[
            ("qualitative", "Qualitative"),
            ("quantitative", "Quantitative"),
        ],
        required=True,
    )
    quantitative_value = fields.Float(
        string="Quantitative Value",
    )
    uom_id = fields.Many2one(
        string="UoM",
        comodel_name="product.uom",
    )
    qualitative_option_id = fields.Many2one(
        string="Qualitative Value",
        comodel_name="measurement.item_type_qualitative_option",
    )
    allowed_qualitative_option_ids = fields.Many2many(
        string="Qualitative Options",
        comodel_name="measurement.item_type_qualitative_option",
        compute="_compute_allowed_qualitative_option_ids",
        store=False,
    )
