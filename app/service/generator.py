# -*- coding: utf-8 -*-
import logging
import os
import re
import xml.etree.ElementTree as ET
from pathlib import Path

import psycopg2
import psycopg2.extras

from .utils import dfs
from app.repository.generator import GeneratorRepository
from app.service.constants import TYPE, SPECIAL_NODES, SPECIAL_NODES_PATTERN
from pkg.db.database import _pool

_logger = logging.getLogger('db-challenge')


class GeneratorService(object):

    def fetch_metadata(self):
        """
        Function fetch db metadata
        :return: data
        """
        try:
            with _pool.getconn() as conn:
                cr = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
                metadata = GeneratorRepository(cr=cr).fetch_metadata()

            _logger.info("[GeneratorService] fetch_metadata success!!")
        finally:
            _pool.putconn(conn)

        return metadata

    def fetch_constraints(self):
        """
        Function fetch db constraint data
        :return: data
        """
        try:
            with _pool.getconn() as conn:
                cr = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
                metadata = GeneratorRepository(cr=cr).fetch_constraints()

            _logger.info("[GeneratorService] fetch_constraints success!!")
        finally:
            _pool.putconn(conn)

        return metadata

    def generate(self):
        """
        :param metadata:
        :return:
        """
        try:
            # fetch metadata
            fetched_data = self.fetch_metadata()
            metadata = {}
            for item in fetched_data:
                metadata.update({
                    item['table']: item.get('metadata', {}),
                })

            # fetch constraints
            fetched_contraints = self.fetch_constraints()
            constraints = {}
            for item in fetched_contraints:
                constraints.update({
                    item['table']: item.get('ref_tables', []),
                })

            # generate
            ordered_tables = self.search(metadata, constraints)
            ordered_data = self.build(metadata, constraints, ordered_tables)
            self.generate_xml(ordered_data)

        except Exception as e:
            _logger.error("ERROR generating xml file: %s" % str(e))
            return False

        _logger.info("[GeneratorService] generate success!!")
        return True

    def search(self, metadata, constraints):
        uniq = set()
        res = []
        for tbl_name, _ in metadata.items():
            dfs(tbl_name, constraints, uniq, res)

        return res

    def build(self, metadata, constraints, ordered_tables):
        res = []
        for tbl_name in ordered_tables:
            data = metadata[tbl_name]
            foreign_data = constraints.get(tbl_name, {})
            if not foreign_data:
                res.append({tbl_name: data})
                continue

            for col in data['columns']:
                if not col['fkey']:
                    continue

                fcols = list(filter(lambda x: x['column_name'] == col['name'], foreign_data))
                if not fcols:
                    continue

                fcol = fcols[0]
                col.update({
                    'ref_column': fcol['foreign_column_name'],
                    'ref_table': fcol['foreign_table_name'],
                })

            res.append({tbl_name: data})

        return res

    def check(self, col_name):
        for node in SPECIAL_NODES:
            for word in SPECIAL_NODES_PATTERN[node]:
                regexp = re.compile(col_name)
                if regexp.search(word):
                    return node

        return None

    def generate_xml(self, ordered_data):
        save_dir_path = '{}/{}'.format(Path(__file__).parent.parent.parent, '/track/xml')
        if not os.path.exists(save_dir_path):
            os.makedirs(save_dir_path)

        save_file_path = '{}/{}'.format(save_dir_path, 'result.xml')
        root = ET.Element('root')
        for d in ordered_data:
            table_name = list(d.keys())[0]
            generate_node = ET.SubElement(root, 'generate')
            generate_node.set('type', table_name)
            columns = d[table_name]['columns']

            # id
            pcols = list(filter(lambda x: x['pkey'] != '', columns))
            if pcols:
                pcol = pcols[0]
                pcol_name = pcol['name']
                pcol_type = pcol['type']
                id_node = ET.SubElement(generate_node, 'id')
                id_node.set('name', pcol_name)
                id_node.set('type', pcol_type)

            # attribute
            acols = list(filter(lambda x: x['pkey'] == '' and x['fkey'] == '', columns))
            for acol in acols:
                acol_name = acol['name']
                acol_type = acol['type']
                mapped_acol_type = TYPE.get(acol_type.upper(), acol_type)
                attribute_name = self.check(acol_name)
                if attribute_name and attribute_name in SPECIAL_NODES:
                    attribute_node = ET.SubElement(generate_node, attribute_name)
                else:
                    attribute_node = ET.SubElement(generate_node, 'attribute')

                attribute_node.set('name', acol_name)
                attribute_node.set('type', mapped_acol_type)

            # reference
            rcols = list(filter(lambda x: x['fkey'] != '', columns))
            for rcol in rcols:
                rcol_name = rcol['name']
                rcol_ref = rcol['ref_column']
                rcol_table = rcol['ref_table']
                reference_node = ET.SubElement(generate_node, 'reference')
                reference_node.set('name', rcol_name)
                reference_node.set('selector', 'select %s from %s' % (rcol_ref, rcol_table))
                reference_node.set('distribution', 'random')

        # write
        tree = ET.ElementTree(root)
        ET.indent(root, space="\t", level=0)
        tree.write(save_file_path, encoding="utf-8")

        return
