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

class StockPicking(orm.Model):
    """ Model name: StockPicking
    """
    
    _inherit = 'stock.picking'

    def do_corresponding(self, cr, uid, ids, context=None):
        ''' Do correspond unload
        '''
        assert len(ids) == 1, 'Works only with one record a time'
        
        # Set move as done:
        move_pool = self.pool.get('stock.move')
        move_ids = move_pool.search(cr, uid, [
            ('picking_id', '=', ids[0]),            
            ], context=context)
        move_pool.write(cr, uid, move_ids, {
            'state': 'done',
            }, context=context)    
        
        # Set document as done:    
        self.write(cr, uid, ids, {
            'correspond': True,
            'state': 'done',
            }, context=context)
        return True 
        #self.do_enter_transfer_details(cr, uid, ids, context=context)
    
    _columns = {
        'correspond': fields.boolean('Correspond document'),
        }
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
