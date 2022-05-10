# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import base64
import csv
from tempfile import TemporaryFile

from openerp import api, fields, models


class MeasurementImport(models.TransientModel):
    _name = "measurement.import"
    _description = "Measurement Import Common Feature"

    data = fields.Binary(string="File", required=True)

    state = fields.Selection(
        string="State",
        selection=[("draft", "draft"), ("success", "success"), ("failed", "failed")],
        default="draft",
    )

    @api.multi
    def _get_obj_item_name(self):
        self.ensure_one()

        return False

    @api.multi
    def _import(self):
        model_item_name = self._get_obj_item_name()
        if not model_item_name:
            return False
        obj_item = self.env[model_item_name]
        fileobj = TemporaryFile("w+")
        fileobj.write(base64.decodestring(self.data))
        fileobj.seek(0)

        reader = csv.reader(fileobj, delimiter=",")
        reader.next()  # noqa: B305

        for row in reader:
            name = row[0]
            item_name = row[3]
            value = row[4]

            criteria = [
                ("measurement_id.name", "=", name),
                ("item_type_id.name", "=", item_name),
            ]
            item_id = obj_item.search(criteria)
            if item_id:
                state = item_id.measurement_id.state
                if state == "open":
                    item_type_id = item_id.item_type_id
                    if item_type_id.question_type == "quantitative":
                        item_id.write({"quantitative_value": value})
            else:
                fileobj.close()
                return False

        fileobj.close()

        return True

    @api.multi
    def button_import(self):
        self.ensure_one()
        data = self._import()
        if data:
            vals = {
                "state": "success",
            }
        else:
            vals = {
                "state": "failed",
            }
        self.write(vals)

        return {
            "type": "ir.actions.act_window",
            "res_model": str(self._model),
            "view_mode": "form",
            "view_type": "form",
            "res_id": self.id,
            "views": [(False, "form")],
            "target": "new",
        }
