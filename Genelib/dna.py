#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
import time

class DNA:
    base_path = "/usr/local"
    install_path = base_path + "/opt"
    download_path = "/var/tmp/gene_downdloads"

    def _inter(self, s):
        return s.format(**sys._getframe(1).f_locals)

    def _exec(self, cmd):
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result
