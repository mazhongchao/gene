#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
import importlib
import alias

def main():
    args = sys.argv
    if len(args) <= 1:
        print 'type gen -h for help'
    elif len(args) == 3 and args[1] == 'install':
        key = args[2]
        if key in alias.libalias:
            c = alias.libalias[key]
            package = importlib.import_module("Genelib."+key)
            tmp_class = getattr(package, c)
            lib = tmp_class()
            lib.install()
        else:
            print 'Lib was not found';

if __name__ == '__main__':
    main()
