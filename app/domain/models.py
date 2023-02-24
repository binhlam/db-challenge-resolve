from dataclasses import dataclass
from typing import List
from app.service.constants import TYPE, SPECIAL_NODES, SPECIAL_NODES_PATTERN
import enum, re


class GeneratorTypes(enum.Enum):
    xml = "xml"
    pdf = "pdf"


class Kinds(enum.Enum):
    id = "id"
    attribute = "attribute"
    reference = "reference"
    hash = "hash"
    encrypt = "encrypt"
    mask = "mask"


@dataclass
class EntityNode:
    name: str
    kind: Kinds = None
    type: str = ""
    selector: str = ""
    distribution: str = "random"


@dataclass
class GenerateNode:
    type: str
    entity_nodes: List[EntityNode] = None


@dataclass
class XmlGenerator:
    root: str
    generate_nodes: List[GenerateNode] = None


class Generator:
    def __init__(self, generator_type=None, data=None):
        self.object = None
        if generator_type == GeneratorTypes.xml.value:
            self.object = self.build_xml_object(data)

    @staticmethod
    def check(col_name):
        for node in SPECIAL_NODES:
            for word in SPECIAL_NODES_PATTERN[node]:
                regexp = re.compile(col_name)
                if regexp.search(word):
                    return node

        return None

    @staticmethod
    def get_kind(attr):
        for kind in Kinds:
            if attr == kind.value:
                return kind

        return Kinds.attribute

    def build_xml_object(self, data):
        xml = XmlGenerator(root="root", generate_nodes=[])
        for d in data:
            table_name = list(d.keys())[0]
            generate_node = GenerateNode(type=table_name, entity_nodes=[])
            columns = d[table_name]['columns']

            # id
            p_cols = list(filter(lambda x: x['pkey'] != '', columns))
            if p_cols:
                pcol = p_cols[0]
                pcol_name = pcol['name']
                pcol_type = pcol['type']
                id_node = EntityNode(name=pcol_name, type=pcol_type, kind=Kinds.id)
                generate_node.entity_nodes.append(id_node)

            # attribute
            a_cols = list(filter(lambda x: x['pkey'] == '' and x['fkey'] == '', columns))
            for acol in a_cols:
                acol_name = acol['name']
                acol_type = acol['type']
                attr_name = self.check(acol_name)
                attr_node = EntityNode(name=acol_name, type=acol_type, kind=Kinds.attribute)
                if attr_name and attr_name in SPECIAL_NODES:
                    attr_node.kind = self.get_kind(attr_name)

                generate_node.entity_nodes.append(attr_node)

            # reference
            r_cols = list(filter(lambda x: x['fkey'] != '', columns))
            for rcol in r_cols:
                rcol_name = rcol['name']
                rcol_ref = rcol['ref_column']
                rcol_table = rcol['ref_table']
                ref_node = EntityNode(
                    name=rcol_name, kind=Kinds.reference,
                    selector='select %s from %s' % (rcol_ref, rcol_table),
                    distribution='random')
                generate_node.entity_nodes.append(ref_node)

            xml.generate_nodes.append(generate_node)

        return xml
