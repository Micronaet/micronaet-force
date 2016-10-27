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
import os
import sys
import logging
import openerp
import openerp.netsvc as netsvc
import openerp.addons.decimal_precision as dp
from openerp.osv import fields, osv, expression, orm
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from openerp import SUPERUSER_ID, api
from openerp import tools
from openerp.tools.translate import _
from openerp.tools.float_utils import float_round as round
from openerp.tools import (DEFAULT_SERVER_DATE_FORMAT, 
    DEFAULT_SERVER_DATETIME_FORMAT, 
    DATETIME_FORMATS_MAP, 
    float_compare)


_logger = logging.getLogger(__name__)


class PurchaseOrder(orm.Model):
    """ Model name: Purchase 
    """    
    _inherit = 'purchase.order'
    
    # -------------
    # Button event:
    # -------------
    def force_purchase_expected(self, cr, uid, ids, context=None):
        ''' Force discount on all lines
        '''
        assert len(ids) == 1, 'Button only for one record a time!'

        # Pool used:
        line_pool = self.pool.get('purchase.order.line')
        move_pool = self.pool.get('stock.move')
        
        force_proxy = self.browse(cr, uid, ids, context=context)[0]
        for line in force_proxy.order_line:
            move_ids = move_pool.search(cr, uid, [
                ('state', '=', 'assigned'),
                ('purchase_line_id', '=', line.id),
                ], context=context)
            if not move_ids:    
                _logger.warning('Line not found for update expected date')
                continue                
            move_pool.write(cr, uid, move_ids, {
                'date_expected': line.date_planned,
                }, context=context)
        return True

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
