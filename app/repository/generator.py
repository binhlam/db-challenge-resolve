# -*- coding: utf-8 -*-
import psycopg2
import psycopg2.extras


class GeneratorRepository:
    def __init__(self, pool=None, logger=None):
        self.pool = pool
        self.logger = logger

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
        try:
            self.logger.info("[GeneratorRepository] fetch_metadata sql: %s" % sql)
            with self.pool.getconn() as conn:
                cr = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
                cr.execute(sql)
                data = cr.fetchall()
        except Exception as e:
            data = None
            self.logger.error("[GeneratorRepository] fetch_metadata error: %s" % str(e))
        finally:
            conn.reset()
            self.pool.putconn(conn)

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
        try:
            self.logger.info("[GeneratorRepository] fetch_constraints sql: %s" % sql)
            with self.pool.getconn() as conn:
                cr = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
                cr.execute(sql)
                data = cr.fetchall()
        except Exception as e:
            data = None
            self.logger.error("[GeneratorRepository] fetch_constraints error: %s" % str(e))
        finally:
            conn.reset()
            self.pool.putconn(conn)

        return data
