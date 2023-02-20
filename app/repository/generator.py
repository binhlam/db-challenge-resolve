# -*- coding: utf-8 -*-
import logging

_logger = logging.getLogger('db-challenge')


class GeneratorRepository(object):
    def __init__(self, cr=None):
        self.cr = cr

    def fetch_metadata(self):
        sql = """
            SELECT
            col.table_name as table,
            json_build_object(
                'columns', json_agg(
                    json_build_object(
                        'name', col.column_name,
                        'type', col.data_type,
                        'pkey', (
                            case
                                when attr.column_index like '%pkey%' then attr.column_index
                                else ''
                            end),
                        'fkey', (
                            case
                                when attr.column_index like '%fki%' then attr.column_index
                                else ''
                            end)
                    )
                )
            ) as metadata
            FROM information_schema.columns col
            LEFT JOIN (
                select distinct
                    tbl.relname as table_name,
                    attr.attname as column_name,
                    col.relname as column_index
                from pg_class tbl
                join pg_attribute attr on attr.attrelid = tbl.oid
                join pg_index idx    on tbl.oid = idx.indrelid AND attr.attnum = ANY(idx.indkey)
                join pg_class col     on col.oid = idx.indexrelid
                where tbl.relkind = 'r'
            ) attr on attr.table_name = col.table_name and attr.column_name = col.column_name
            where table_schema='public'
            group by col.table_name;
        """
        data = None
        try:
            self.cr.execute(sql)
            data = self.cr.fetchall()
        except Exception as e:
            _logger.error("[GeneratorRepository] fetch error: %s" % str(e))

        return data

    def fetch_constraints(self):
        sql = """
            SELECT
                tc.table_name as table,
                json_agg(
                    json_build_object(
                            'column_name', kcu.column_name,
                            'foreign_column_name', ccu.column_name,
                            'foreign_table_name', ccu.table_name
                        )
                ) as ref_tables
            FROM
                information_schema.table_constraints AS tc
                INNER JOIN information_schema.key_column_usage AS kcu
                    ON tc.constraint_name = kcu.constraint_name AND tc.table_schema = kcu.table_schema
                INNER JOIN information_schema.constraint_column_usage AS ccu
                    ON ccu.constraint_name = tc.constraint_name AND ccu.table_schema = tc.table_schema
            WHERE tc.constraint_type = 'FOREIGN KEY'
              AND tc.table_schema='public'
            GROUP BY tc.table_name
        """
        data = None
        try:
            self.cr.execute(sql)
            data = self.cr.fetchall()
        except Exception as e:
            _logger.error("[GeneratorRepository] fetch constraints: %s" % str(e))

        return data
