# All rights reserved (c) 2019-2020, Vladimir Botka <vbotka@gmail.com>
# Simplified BSD License, https://opensource.org/licenses/BSD-2-Clause

import sys
import json

def list_flatten(l):
    flat_list = []
    for sublist in l:
        if isinstance(sublist, (list,)):
            for item in sublist:
                flat_list.append(item)
        else:
            flat_list.append(sublist)
    l = flat_list
    return l

def dict_merge(x, y):
    d = x.copy()
    d.update(y)
    return d

def dict_merge_lossless(x, y):
    d = x.copy()
    d.update(y)
    for key, value in d.items():
       if key in x and key in y:
               d[key] = [value , x[key]]
    return d

def dict_add_dict(d1, d2, recursive=False):
    if recursive:
        for k, v in d2.items():
            d1[k] = [d1[k],v]
    else:
        for k, v in d2.items():
            d1[k] = v
    if isinstance(d1[k], (list,)):
        d1[k] = list_flatten(d1[k])
    return d1

def dict_del_key(d, key):
    del d[key]
    return d

def dict_keys(d):
    return list(d)

def dict_sorted(d):
    return sorted(d)

def dict_search_key(d, key):
    return key in d

def dict_prefix_keys(d, prefix='prefix_'):
    d1 = {}
    for key in d.keys():
        d1[prefix + key] = d[key]
    return d1

def dict_flatten(d, separator='.'):
    ''' Credit: Flattening JSON objects in Python by Amir Ziai
        https://towardsdatascience.com/flattening-json-objects-in-python-f5343c794b10'''
    out = {}
    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + separator)
        elif type(x) is list:
            i = 0
            for a in sorted(x):
                flatten(a, name + str(i) + separator)
                i += 1
        else:
            out[name[:-1]] = x
    flatten(d)
    return out

def dict_sortbysubkey(d, k):
    return sorted(d.items(), key=lambda x: x[1][k])

def dict2list(d):
    l = []
    for i in d:
        h = {i:d[i]}
        l.append(h)
    return l

def item2dict(t):
    h = {t[0]:t[1]}
    return h

def dict_select_list(d, l):
    d2 = {}
    for k in l:
        d2[k] = d[k]
    return d2

def dict2hash(d):
    return hash(json.dumps(d, sort_keys=True)) % ((sys.maxsize + 1) * 2)

def dict_add_hash(d, k='hash'):
    d2 = d
    d2[k] = hash(json.dumps(d, sort_keys=True))
    return d2

class FilterModule(object):
    ''' Ansible filters. Interface to Python dictionary methods.

        5.5. Dictionaries
        https://docs.python.org/3/tutorial/datastructures.html#dictionaries'''

    def filters(self):
        return {
            'dict_add_dict': dict_add_dict,
            'dict_del_key': dict_del_key,
            'dict_keys': dict_keys,
            'dict_merge': dict_merge,
            'dict_merge_lossless': dict_merge_lossless,
            'dict_sorted': dict_sorted,
            'dict_search_key': dict_search_key,
            'dict_prefix_keys': dict_prefix_keys,
            'dict_flatten': dict_flatten,
            'dict_sortbysubkey': dict_sortbysubkey,
            'dict2list': dict2list,
            'item2dict': item2dict,
            'dict_select_list': dict_select_list,
            'dict2hash': dict2hash,
            'dict_add_hash': dict_add_hash
        }
