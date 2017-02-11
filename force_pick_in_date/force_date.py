# -*- coding: utf-8 -*-
###############################################################################
#
#    Copyright (C) 2001-2014 Micronaet SRL (<http://www.micronaet.it>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################
from openerp import models, fields, api
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
from datetime import datetime


class stock_transfer_details(models.TransientModel):
    _inherit = 'stock.transfer_details'

    @api.one
    def do_detailed_transfer(self):
        import pdb; pdb.set_trace()
        super(stock_transfer_details, self).do_detailed_transfer()
        import pdb; pdb.set_trace()
        self.picking_id.write({'date': datetime.now()})
        return True
        
    """def do_detailed_transfer(self, cr, uid, ids, context=None)
        res = super(stock_transfer_details, self).do_detailed_transfer(
            cr, uid, ids, context=context)
        
        # Update picking date:
        current_proxy = self.browse(cr, uid, ids, context=context)[0]
        self.pool.get('stock.picking').write(cr, uid, current_proxy.picking_id.id, {
            'date': datetime.now(),
            }, context=context)
        return res    
        self.picking_id.do_transfer()

        return True"""
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
