# -*- coding: utf-8 -*-
import os
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from .utils import dfs
from app.service.constants import TYPE, SPECIAL_NODES, SPECIAL_NODES_PATTERN
from ..domain.models import Generator
from app.service.xml.generator import XmlGenerator


class GeneratorService:
    def __init__(self, repo=None, logger=None):
        self.repo = repo
        self.logger = logger

    def fetch_metadata(self):
        """
        Function fetch db metadata
        :return: data
        """

        metadata = self.repo.fetch_metadata()
        if not metadata:
            self.logger.error("[GeneratorService] fetch_metadata error")
            return None

        return metadata

    def fetch_constraints(self):
        """
        Function fetch db constraint data
        :return: data
        """
        metadata = self.repo.fetch_constraints()
        if not metadata:
            self.logger.error("[GeneratorService] fetch_constraints error")
            return None

        return metadata

    @staticmethod
    def search(metadata, constraints):
        uniq = set()
        res = []
        for tbl_name, _ in metadata.items():
            dfs(tbl_name, constraints, uniq, res)

        return res

    @staticmethod
    def build(metadata, constraints, ordered_tables):
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

    def generate(self):
        """
        :param:
        :return:
        """
        try:
            # fetch metadata
            fetched_data = self.fetch_metadata()
            if not fetched_data:
                self.logger.error("[GeneratorService] generate error")
                return None

            metadata = {}
            for item in fetched_data:
                metadata.update({
                    item['table']: item.get('metadata', {}),
                })

            # fetch constraints
            fetched_contraints = self.fetch_constraints()
            if not fetched_data:
                self.logger.error("[GeneratorService] generate error")
                return None

            constraints = {}
            for item in fetched_contraints:
                constraints.update({
                    item['table']: item.get('ref_tables', []),
                })

            # build data
            ordered_tables = self.search(metadata, constraints)
            ordered_data = self.build(metadata, constraints, ordered_tables)

            # build generator
            xml_generator = Generator(generator_type='xml', data=ordered_data)

            # generate
            xml_generator_svc = XmlGenerator(xml_generator)
            xml_generator_svc.generate()

        except Exception as e:
            self.logger.error("[GeneratorService] generating xml file error: %s" % str(e))
            return False

        self.logger.info("[GeneratorService] generate success!!")
        return True
