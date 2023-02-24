from pathlib import Path
from app.domain.models import Kinds
from app.service.constants import TYPE
import os
import xml.etree.ElementTree as ET

DEFAULT_DIR_PATH = '{}/{}'.format(Path(__file__).parent.parent.parent.parent, '/track/xml')


class XmlGenerator:
    def __init__(self, generator=None, save_dir_path=None):
        self.generator = generator.object
        if not save_dir_path:
            self.save_dir_path = DEFAULT_DIR_PATH
        else:
            self.save_dir_path = save_dir_path

    def generate(self):
        if not os.path.exists(self.save_dir_path):
            os.makedirs(self.save_dir_path)

        save_file_path = '{}/{}'.format(self.save_dir_path, 'result.xml')
        root = ET.Element(self.generator.root)
        for gen in self.generator.generate_nodes:
            generate_node = ET.SubElement(root, 'generate')
            generate_node.set('type', gen.type)

            for ent in gen.entity_nodes:
                ent_type = TYPE.get(ent.type.upper(), ent.type)

                # id
                if ent.kind == Kinds.id:
                    id_node = ET.SubElement(generate_node, Kinds.id.value)
                    id_node.set('name', ent.name)
                    id_node.set('type', ent_type)
                    continue

                # reference
                if ent.kind == Kinds.reference:
                    reference_node = ET.SubElement(generate_node, Kinds.reference.value)
                    reference_node.set('name', ent.name)
                    reference_node.set('selector', ent.selector)
                    reference_node.set('distribution', ent.distribution)
                    continue

                # entity
                attribute_node = ET.SubElement(generate_node, ent.kind.value)
                attribute_node.set('name', ent.name)
                attribute_node.set('type', ent_type)

        # write
        tree = ET.ElementTree(root)
        ET.indent(root, space="\t", level=0)
        tree.write(save_file_path, encoding="utf-8")

        return
