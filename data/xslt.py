"""
XSLT script to transform DM&D into GNU Health XML
"""
import sys

import ffs
from lxml import etree

HERE = ffs.Path.here()
DRUGFILE = HERE/'f_amp2_3281113.xml'

XML = """<?xml version="1.0" encoding="utf-8"?>
<tryton>
<data noupdate="1">

<!-- WE ADD THE BASIC PRODUCTS RELATED TO THE MEDICAMENTS -->

<!-- Add basic category -->
<record model="product.category" id="prod_medicament">
    <field name="name">Medicaments</field>
</record>
<record model="product.category" id="prod_medicament_DMD">
    <field name="name">DM+D Medicines</field>
    <field name="parent" ref="prod_medicament"/>
</record>

<!-- PRODUCT TEMPLATE DEFINITION -->
{templates}

<!-- PRODUCT DEFINITION -->
{products}

</data>
</tryton>
"""

XML_TEMPLATE_TEMPLATE = """
<record model="product.template" id="templ_em{num}">
    <field name="name">{name}</field>
    <field name="category" model="product.category" ref="prod_medicament_DMD"/>
    <field name="default_uom" model="product.uom" ref="product.uom_unit"></field>
    <field name="list_price" eval="0.0"/>
    <field name="cost_price" eval="0.0"/>
</record>
"""

XML_PRODUCT_TEMPLATE = """
<record model="product.product" id="prod_em{num}">
    <field name="template" model="product.template" ref="templ_em{num}"/>
    <field name="is_medicament">1</field>
</record>
"""

def main():
    templates, products = [], []
    root = etree.fromstring(DRUGFILE.contents)
    for num, drug in enumerate(root.findall('AMPS/AMP'), 1):
        name = drug.find('NM').text.replace('&', 'and')

        templates.append(XML_TEMPLATE_TEMPLATE.format(num=num, name=name))
        products.append(XML_PRODUCT_TEMPLATE.format(num=num))

    outfile = XML.format(templates="\n".join(templates),
                         products="\n".join(products))
    print outfile

    return 0

if __name__ == '__main__':
    sys.exit(main())
