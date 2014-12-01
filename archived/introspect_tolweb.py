#!/:usr/bin/env python
from xml.etree import ElementTree as ET
doc = ET.parse('tolweb.xml')
tree = doc.getroot()

_SCHEMA = {}
def introspect(el):
    tag = el.tag
    d = _SCHEMA.setdefault(tag, {})
    a = d.setdefault('attrib', {})
    for k, v in el.attrib.items():
        old_v = a.setdefault(k, {})
        if len(old_v) < 10:
            old_v[v] = 1 + old_v.get(v, 0)
    ch = d.setdefault('children', set())
    for c in el:
        ch.add(c.tag)
        introspect(c)
introspect(tree)
for k, v in _SCHEMA.items():
    print k, 'attributes ='
    for ak, d in v['attrib'].items():
        if len(d) < 10:
            for av, ac in d.items():
                print '   attrib ', ak, str(av), 'count =', ac
        else:
            print '   attrib', ak, d.keys()
    print k, 'children =', v['children']
    print