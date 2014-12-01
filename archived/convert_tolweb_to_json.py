#!/:usr/bin/env python
from xml.etree import ElementTree as ET
from bs4 import BeautifulSoup
import codecs
import sys
import os

err_stream_fn = 'convert_tolweb_to_json-ERR-MESSAGES.txt'
output_fn = 'tolweb.json'
if os.path.exists(output_fn):
    sys.exit('output file "{}" already exists. delete it to run this.\n'.format(output_fn))
doc = ET.parse('tolweb.xml')
tree = doc.getroot()


class ListOf(object):
    def __init__(self, contained):
        self.contained = contained
class ID(int):
    pass
TwoBool = object()
TEXT = object()
_SCHEMA = {
    'NODE': [{
        'CONFIDENCE': range(3),
        'LEAF': bool,
        'SHOWAUTHORITYCONTAINING': bool,
        'ANCESTORWITHPAGE': ID,
        'IS_NEW_COMBINATION': bool,
        'ITALICIZENAME': bool,
        'CHILDCOUNT': int,
        'INCOMPLETESUBGROUPS': bool,
        'PHYLESIS' : range(3),
        'HASPAGE': bool,
        'COMBINATION_DATE': int,
        'EXTINCT': TwoBool,
        'SHOWAUTHORITY': bool,
        'ID': ID },
        set(['NAME', 'AUTHDATE', 'NAMECOMMENT', 'COMBINATION_AUTHOR', 'AUTHORITY', 'OTHERNAMES', 'NODES', 'DESCRIPTION'])],
    'NAME': TEXT,
    'AUTHDATE': TEXT,
    'NAMECOMMENT': TEXT,
    'OTHERNAME': [{
        'DATE': int,
        'ISIMPORTANT': bool,
        'ISPREFERRED': bool,
        'ITALICIZENAME': bool,
        'SEQUENCE': int},
        set(['COMMENTS', 'NAME', 'AUTHORITY'])],
    'COMBINATION_AUTHOR': TEXT,
    'TREE': [{}, ['NODE']],
    'AUTHORITY': TEXT,
    'OTHERNAMES': ListOf('OTHERNAME'),
    'COMMENTS': TEXT,
    'NODES': ListOf('NODE'),
    'DESCRIPTION': TEXT,
}

rename = {'ITALICIZENAME': 'italicizeName',
     'COMMENTS': 'comments',
     'DATE': 'year',
     'ISIMPORTANT': 'isImportant',
     'NODES': 'nodes',
     'AUTHDATE': 'authDate',
     'ANCESTORWITHPAGE': 'ancestorWithPage',
     'CHILDCOUNT': 'childCount',
     'OTHERNAMES': 'otherNames',
     'INCOMPLETESUBGROUPS': 'incompleteSubgroups',
     'EXTINCT': 'extinct',
     'SHOWAUTHORITY': 'showAuthority',
     'NODE': 'node',
     'SEQUENCE': 'sequence',
     'COMBINATION_AUTHOR': 'combinationAuthor',
     'IS_NEW_COMBINATION': 'isNewCombination',
     'PHYLESIS': 'phylesis',
     'HASPAGE': 'hasPage',
     'COMBINATION_DATE': 'combinationDate',
     'ID': 'ID',
     'NAME': 'name',
     'CONFIDENCE': 'confidence',
     'LEAF': 'isLeaf',
     'DESCRIPTION': 'description',
     'NAMECOMMENT': 'nameComment',
     'SHOWAUTHORITYCONTAINING': 'showAuthorityContaining',
     'OTHERNAME': 'otherName',
     'TREE': 'tree',
     'AUTHORITY': 'authority',
     'ISPREFERRED': 'isPreferred'}
err_stream = codecs.open(err_stream_fn, 'w', encoding='utf-8')

def validate(el):
    tag = el.tag
    type_def = _SCHEMA[tag]
    if isinstance(type_def, ListOf):
        assert list(el.attrib.items()) == []
        for sub in el:
            assert sub.tag == type_def.contained
            validate(sub)
    else:
        attrib_def, sub_el = type_def
        expected_att = attrib_def.keys()
        for k, v in el.attrib.items():
            assert k in expected_att
            expected_att.remove(k)
        assert len(expected_att) == 0
        for sub in el:
            assert sub.tag in sub_el    
            validate(sub)
#validate(tree)
import sys
def coerce_tol(s, expected):
    if expected is TwoBool:
        assert s in '02'
        return s == '2'
    elif expected is bool:
        assert s in '01'
        return s == '1'
    elif isinstance(expected, list):
        i = int(s)
        assert i < len(expected)
        return i
    elif expected is int:
        if s == 'null':
            return None
        return int(s)
    elif expected is ID:
        return int(s)

NODE_DEFAULTS = {
    'confidence': 0,
    'isLeaf': False,
    'showAuthorityContaining': False,
    'isNewCombination': False,
    'italicizeName': False,
    'incompleteSubgroups': False,
    'phylesis': 0,
    'hasPage': False,
    'extinct': False,
    'showAuthority': False,
    'authDate': "null",
    'date': "null",
    'year': "null",
    'isPreferred': False,
    'isImportant':False,
}
POS_ZERO_NULL = ['authDate', 'description']
def del_if_default(node):
    for k, default in NODE_DEFAULTS.items():
        if (k in node) and (node.get(k) == default):
            del node[k]
    for k in POS_ZERO_NULL:
        if node.get(k) == '0':
            del node[k]
    if 'childCount' in node:
        assert node['childCount'] == len(node.get('nodes', []))
        del node['childCount']
def clean_html(r):
    if isinstance(r, str) or isinstance(r, unicode):
        if '&' in r:
            f = r.replace('&lt;', '<').replace('&gt;', '>')
            f = f.replace('&amp;lt;', '<').replace('&amp;gt;', '>')
            f = f.replace('&amp;amp;', '&')
            rr = BeautifulSoup(f).text
            err_stream.write(u'Replacing "{}"\nwith       "{}"\n'.format(r, rr))
            r = rr
    return r
def convert(el):
    d_el = {}
    tag = el.tag
    type_def = _SCHEMA[tag]
    if type_def is TEXT:
        t = el.text
        if t is None:
            return None
        return t.strip()
    if isinstance(type_def, ListOf):
        assert list(el.attrib.items()) == []
        d_el = []
        for sub in el:
            assert sub.tag == type_def.contained
            d_el.append(convert(sub))
        if tag == 'OTHERNAMES':
            # order by "SEQUENCE" and discard that field
            r = [None]*len(d_el)
            for on_el in d_el:
                ind = on_el['sequence']
                assert r[ind] is None
                r[ind] = on_el
                del on_el['sequence']
            return r
        return d_el
    else:
        attrib_def, sub_el = type_def
        expected_att = attrib_def.keys()
        for k, v in el.attrib.items():
            assert k in expected_att
            conv_name = rename[k]
            assert conv_name not in d_el
            #sys.stderr.write(el.tag + ' ' + k + '\n')
            r = coerce_tol(v, attrib_def[k])
            if r is not None:
                d_el[conv_name] = clean_html(r)
        for sub in el:
            assert sub.tag in sub_el
            conv_name = rename[sub.tag]
            assert conv_name not in d_el
            r = convert(sub)
            if r is not None:
                r = clean_html(r)
                d_el[conv_name] = r
    if tag == 'NODE' or tag == 'OTHERNAME':
        del_if_default(d_el)
    return d_el
j = convert(tree)
t = {'nodes': [j['node']]}
import json
with codecs.open(output_fn, 'w', encoding='utf-8') as fo:
    json.dump(t, fo, indent=0, sort_keys=True, separators=(',', ': '))
