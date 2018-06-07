#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
import time

class DNA:
    base_path = "/usr/local"
    install_path = base_path + "/opt"
    download_path = "/usr/local/src/gene_downdloads"

    def _inter(self, s):
        return s.format(**sys._getframe(1).f_locals)

    def _exec(self, cmd):
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    def _set_centos_startup(self, file_name):
        content = """
            [Unit]
            Description=php
            After=network.target
            [Service]
            Type=forking
            ExecStart=/usr/local/php/sbin/php-fpm
            ExecStop=/bin/pkill -9 php-fpm
            PrivateTmp=true
            [Install]
            WantedBy=multi-user.target
            """
        service = "/usr/lib/systemd/system/" + file_name + ".service"
        fw = open(service, "w");
        fw.write(content);
        fw.close

    def _set_ubuntu_startup(self, file_name):
        content = """
            [Unit]
            Description=php
            After=network.target
            [Service]
            Type=forking
            ExecStart=/usr/local/php/sbin/php-fpm
            ExecStop=/bin/pkill -9 php-fpm
            PrivateTmp=true
            [Install]
            WantedBy=multi-user.target
            """
        service = "/usr/lib/systemd/system/" + file_name + ".service"
        fw = open(service, "w");
        fw.write(content);
        fw.close
