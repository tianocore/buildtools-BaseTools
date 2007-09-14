class sdict(dict):
    def __init__(self):
        self._key_list = []

    def __setitem__(self, key, value):
        if key not in self._key_list:
            self._key_list.append(key)
        dict.__setitem__(self, key, value)

    def __delitem__(self, key):
        self._key_list.remove(key)
        dict.__delitem__(self, key)
    #
    # used in "for k in dict" loop to ensure the correct order
    #
    def __iter__(self):
        return self.iterkeys()

    def __len__(self):
        return len(self._key_list)

    def __contains__(self, key):
        return key in self._key_list

    def has_key(self, key):
        return key in self._key_list

    def clear(self):
        self._key_list = []
        dict.clear(self)

    def keys(self):
        keys = []
        for key in self._key_list:
            keys.append(key)
        return keys

    def values(self):
        values = []
        for key in self._key_list:
            values.append(self[key])
        return values

    def items(self):
        items = []
        for key in self._key_list:
            items.append((key, self[key]))
        return items

    def iteritems(self):
        return iter(self.items())

    def iterkeys(self):
        return iter(self.keys())

    def itervalues(self):
        return iter(self.values())

    def pop(self, key, *dv):
        value = None
        if key in self._key_list:
            value = self[key]
            dict.__delitem__(self, key)
        elif len(dv) != 0 :
            value = kv[0]
        return value

    def popitem(self):
        key = self._key_list[0]
        value = self[key]
        dict.__delitem__(self, key)
        return key, value

# This acts like the main() function for the script, unless it is 'import'ed into another
# script.
if __name__ == '__main__':
    sd = sdict()
    print "#### 11111111111 ###"
    sd["abc"] = 1
    sd['efg'] = 2
    sd['hij'] = 3
    print "for key in dict (%d) =" % len(sd),
    for key in sd:
        print "(",key, sd[key],")",
    print
    print "keys() =",sd.keys()
    print "values() =",sd.values()
    print "items() =",sd.items()
    print "iterkeys() =",[k for k in sd.iterkeys()]
    print "itervalues() =",[v for v in sd.itervalues()]
    print "iteritems() =",[i for i in sd.iteritems()]
    print sd

    print "#### 22222222222 ###"
    sd.clear()
    sd['efg'] = 1
    sd['hij'] = 2
    sd["abc"] = 3
    print "for key in dict (%d) =" % len(sd),
    for key in sd:
        print "(",key, sd[key],")",
    print
    print "keys() =",sd.keys()
    print "values() =",sd.values()
    print "items() =",sd.items()
    print "iterkeys() =",[k for k in sd.iterkeys()]
    print "itervalues() =",[v for v in sd.itervalues()]
    print "iteritems() =",[i for i in sd.iteritems()]
    print sd

    print "#### 33333333333 ###"
    sd.clear()
    sd['hij'] = 1
    sd["abc"] = 2
    sd['efg'] = 3
    print "for key in dict (%d) =" % len(sd),
    for key in sd:
        print "(",key, sd[key],")",
    print
    print "keys() =",sd.keys()
    print "values() =",sd.values()
    print "items() =",sd.items()
    print "iterkeys() =",[k for k in sd.iterkeys()]
    print "itervalues() =",[v for v in sd.itervalues()]
    print "iteritems() =",[i for i in sd.iteritems()]
    print sd

    print "#### 44444444444 ###"
    sd["abc"] = 1
    sd['efg'] = 2
    sd['hij'] = 3
    print "for key in dict (%d) =" % len(sd),
    for key in sd:
        print "(",key, sd[key],")",
    print
    print "keys() =",sd.keys()
    print "values() =",sd.values()
    print "items() =",sd.items()
    print "iterkeys() =",[k for k in sd.iterkeys()]
    print "itervalues() =",[v for v in sd.itervalues()]
    print "iteritems() =",[i for i in sd.iteritems()]
    print sd

    if sdict() == {}:
        print "Empty sdict equals to {}. No need to override the __eq__()"
    else:
        print "Empty sdict doesn't equal to {}. sdict needs to override the __eq__()"
