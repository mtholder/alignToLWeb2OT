#!/usr/bin/env python
import weakref
import codecs
import json
import sys
import os
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)
from peyotl.ott import OTT
ott = OTT()
json_file = 'tolweb.json'
with codecs.open(json_file, 'r', encoding='utf-8') as jo:
    tol_blob = json.load(jo)
_EMPTY_TUPLE = tuple()
class ToLWebOtherName(object):
    def __init__(self, as_dict, par):
        self._d = as_dict
        self._node = par
    @property
    def date(self):
        return self._d.get('year')
    @property
    def year(self):
        return self._d.get('year')
    @property
    def is_important(self):
        return self._d.get('isImportant', False)
    @property
    def is_preferred(self):
        return self._d.get('isPreferred', False)
    @property
    def italicize_name(self):
        return self._d.get('italicizeName', False)
    @property
    def sequence(self):
        return self._node._other_names.index(self)
    @property
    def comments(self):
        return self._d.get('comments')
    @property
    def name(self):
        return self._d.get('name')
    @property
    def authority(self):
        return self._d.get('authority')
    @property
    def italicize_name(self):
        return self._d.get('italicizeName', False)

class ToLWebNode(object):
    def __init__(self, as_dict, id2node):
        self._d = as_dict
        self._id = as_dict['ID']
        id2node[self._id] = self
        self._parent = None
        c = []
        for child_dict in as_dict.get('nodes', []):
            child = ToLWebNode(child_dict, id2node)
            child._parent = self
            c.append(child)
        if c:
            self._children = tuple(c)
        else:
            self._children = _EMPTY_TUPLE
        o = []
        _sw = None
        for on_dict in as_dict.get('otherNames', []):
            if _sw is None:
                _sw = weakref.proxy(self)
            ono = ToLWebOtherName(on_dict, _sw)
            o.append(ono)
        if o:
            self._other_names = tuple(o)
        else:
            self._other_names = _EMPTY_TUPLE
        if not self._children:
            self.ott_id = ott.get_ott_ids(self.name)
            if self.ott_id is None:
                sys.stderr.write(u'Name not found "{}"\n'.format(self.name))
            elif isinstance(self.ott_id, tuple) and len(self.ott_id) > 1:
                sys.stderr.write(u'Homonym found "{}" -> "{}"\n'.format(self.name, '", "'.join([str(i) for i in self.ott_id])))
            else:
                sys.stderr.write(u'Mapped "{}" -> "{}"\n'.format(self.name, self.ott_id))
                

    @property
    def confidence(self):
        return self._d.get('confidence', 0)
    @property
    def is_leaf(self):
        return self._d.get('isLeaf', False)
    @property
    def show_authority_containint(self):
        return self._d.get('showAuthorityContaining', False)
    @property
    def ancestor_with_page(self):
        return self._d.get('ancestorWithPage')
    @property
    def is_new_combination(self):
        return self._d.get('isNewCombination', False)
    @property
    def ancestor_with_page(self):
        return self._d.get('ancestorWithPage')
    @property
    def italicize_name(self):
        return self._d.get('italicizeName', False)
    @property
    def child_count(self):
        return len(self._children)
    @property
    def incomplete_subgroups(self):
        return self._d.get('incompleteSubgroups', False)
    @property
    def phylesis(self):
        return self._d.get('phylesis', 0)
    @property
    def has_page(self):
        return self._d.get('hasPage', False)
    @property
    def extinct(self):
        return self._d.get('extinct', False)
    @property
    def show_authority(self):
        return self._d.get('showAuthority', False)
    @property
    def id(self):
        return self._id
    @property
    def nodes(self):
        return self._children
    @property
    def children(self):
        return self._children
    @property
    def parent(self):
        return self._parent
    @property
    def name(self):
        return self._d.get('name')
    @property
    def authority(self):
        return self._d.get('authority')
    @property
    def authority_date(self):
        return self._d.get('authDate')
    @property
    def name_comment(self):
        return self._d.get('nameComment')
    @property
    def combination_date(self):
        return self._d.get('combinationDate')
    @property
    def combination_author(self):
        return self._d.get('combinationAuthor')
    @property
    def description(self):
        return self._d.get('description')
    @property
    def other_names(self):
        return self._other_names
class ToLWeb(object):
    def __init__(self, as_dict):
        self._d = as_dict
        root_list = as_dict['nodes']
        assert len(root_list) == 1
        self._id2node = {}
        self._root = ToLWebNode(root_list[0], self._id2node)

tolweb_backbone = ToLWeb(tol_blob)

