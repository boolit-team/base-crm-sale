# -*- encoding: utf-8 -*-
##############################################################################
#    
#    Odoo, Open Source Management Solution
#
#    Author: Andrius Laukavičius. Copyright: JSC NOD Baltic
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.     
#
##############################################################################

from openerp import models
import psycopg2
import logging
import operator
from openerp.tools import mute_logger
_logger = logging.getLogger('base.partner.merge')

class MergePartnerAutomatic(models.TransientModel):
    _inherit = 'base.partner.merge.automatic.wizard'

    def _update_foreign_keys(self, cr, uid, src_partners, dst_partner, context=None):
        _logger.debug('_update_foreign_keys for dst_partner: %s for src_partners: %r', dst_partner.id, list(map(operator.attrgetter('id'), src_partners)))

        # find the many2one relation to a partner
        proxy = self.pool.get('res.partner')
        self.get_fk_on(cr, 'res_partner')

        # ignore two tables

        for table, column in cr.fetchall():
            if 'base_partner_merge_' in table:
                continue
            partner_ids = tuple(map(int, src_partners))

            query = "SELECT column_name FROM information_schema.columns WHERE table_name LIKE '%s'" % (table)
            cr.execute(query, ())
            columns = []
            for data in cr.fetchall():
                if data[0] != column:
                    columns.append(data[0])
            query = "SELECT column_name FROM information_schema.columns WHERE table_name LIKE '%s' AND column_name = 'write_date'" % (table)
            cr.execute(query, ())
            write_date = False
            for data in cr.fetchall():
                write_date = True
            query_dic = {
                'table': table,
                'column': column,
                'value': columns[0],
                'write_date': ", write_date = (now() at time zone 'utc')" if write_date else '',
            }
            if len(columns) <= 1:
                # unique key treated
                query = """
                    UPDATE "%(table)s" as ___tu
                    SET %(column)s = %%s
                    WHERE
                        %(column)s = %%s AND
                        NOT EXISTS (
                            SELECT 1
                            FROM "%(table)s" as ___tw
                            WHERE
                                %(column)s = %%s AND
                                ___tu.%(value)s = ___tw.%(value)s
                        )""" % query_dic
                for partner_id in partner_ids:
                    cr.execute(query, (dst_partner.id, partner_id, dst_partner.id))
            else:
                try:
                    with mute_logger('openerp.sql_db'), cr.savepoint():
                        query = 'UPDATE "%(table)s" SET %(column)s = %%s %(write_date)s WHERE %(column)s IN %%s' % query_dic
                        cr.execute(query, (dst_partner.id, partner_ids,))

                        if column == proxy._parent_name and table == 'res_partner':
                            query = """
                                WITH RECURSIVE cycle(id, parent_id) AS (
                                        SELECT id, parent_id FROM res_partner
                                    UNION
                                        SELECT  cycle.id, res_partner.parent_id
                                        FROM    res_partner, cycle
                                        WHERE   res_partner.id = cycle.parent_id AND
                                                cycle.id != cycle.parent_id
                                )
                                SELECT id FROM cycle WHERE id = parent_id AND id = %s
                            """
                            cr.execute(query, (dst_partner.id,))
                except psycopg2.Error:
                    # updating fails, most likely due to a violated unique constraint
                    # keeping record with nonexistent partner_id is useless, better delete it
                    query = 'DELETE FROM %(table)s WHERE %(column)s = %%s' % query_dic
                    cr.execute(query, (partner_id,))