#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import urllib2
import hashlib
import dna

class PHP(dna.DNA):
    libtag = "php-7.2.5"
    url = "https://php.net/get/php-7.2.5.tar.xz/from/this/mirror"
    desc = "General-purpose scripting language"
    homepage = "https://secure.php.net/"
    sha256 = "af70a33b3f7a51510467199b39af151333fbbe4cc21923bad9c7cf64268cddb2"
    preins_items = {"centos":["openssl-devel.x86_64", "bzip2-devel.x86_64", "libcurl-devel.x86_64",
                    "libpng-devel.x86_64", "freetype-devel.x86_64", "libjpeg-turbo-devel.x86_64",
                    "libmcrypt-devel.x86_64", "unixODBC-devel.x86_64", "unixODBC.x86_64", "libxml2-devel"],
                    "ubuntu":[]
                    }
    os = 'centos'

    def __init__(self, option=[]):
        self.option = option

    def install(self):
        self.file_download()
        if self.file_verify():
            self._before_install()
            self._install()
            self._after_install()

    def _install(self):
        libtag = self.libtag
        (lib, version) = libtag.split("-") # lib="php" version="7.2.5"
        prefix = self.install_path + self._inter("/{lib}/{version}")
        config_path = self.base_path + self._inter("/etc/{lib}/") + version[0:3]
        args = """--prefix={prefix}
                --with-config-file-path={config_path}
                --with-config-file-scan-dir={config_path}/conf.d
                --with-fpm-user=www
                --with-fpm-group=www
                --enable-bcmath
                --enable-calendar
                --enable-dba
                --enable-dtrace
                --enable-exif
                --enable-ftp
                --enable-fpm
                --enable-gd-native-ttf
                --enable-inline-optimization
                --enable-intl
                --enable-mbregex
                --enable-mbstring
                --enable-mysqlnd
                --enable-opcache-file
                --enable-pcntl
                --enable-shmop
                --enable-soap
                --enable-sockets
                --enable-sysvsem
                --enable-sysvshm
                --enable-zip
                --disable-debug
                --disable-rpath
                --with-bz2
                --with-curl
                --with-freetype-dir=/usr/include/freetype2/freetype
                --with-gd
                --with-gettext
                --with-iconv
                --with-jpeg-dir
                --with-libxml-dir
                --with-mhash
                --with-mysql-sock=/tmp/mysql.sock
                --with-mysqli=mysqlnd
                --with-openssl
                --with-pdo-mysql=mysqlnd
                --with-pdo-odbc=unixODBC,/usr
                --with-pcre-regex
                --with-png-dir
                --with-xmlrpc
                --with-xsl
                --with-unixODBC=/usr
                --with-zlib
                --without-pear"""

        print("===> Installing " + self.libtag)
        os.system("cd /var/tmp/gene")

        os.system(self._inter("tar xzf {libtag}.tar.xz"))
        os.system(self._inter("cd {libtag}"))

        args = self._inter(args)
        os.system(self._inter("./configure {args} >> /tmp/gene-install-{libtag}.configure.log"))
        os.system(self._inter("make"))
        os.system(self._inter("make isntall >> /tmp/gene-install-{libtag}.install.log"))

        self._after_install();

    def file_download(self):
        libtag = self.libtag
        download_path = self.download_path

        if not os.path.exists(download_path):
            os.makedirs(download_path)

        print "===> Downloading " + libtag + "from " + self.url
        f = urllib2.urlopen(self.url)
        with open(self._inter("{download_path}/{libtag}.tar.xz", "wb")) as code:
            code.write(f.read())

    def file_verify(self):
        libtag = self.libtag
        download_path = self.download_path
        BUF_SIZE = 65536
        print "===> Verfiying"
        with open(self._inter("{download_path}/{libtag}.tar.xz", "rb")) as f:
            while True:
                data = f.read(BUF_SIZE)
                if not data:
                    break

                if hashlib.sha256(data) == self.sha256:
                    return True
                else:
                    print "===> Verify file " + self.lib + ".tar.xz faild for " + hashlib.sha256(data)
                    return False
        return False

    def echo(self):
        print "Test....PHP"

    def _before_install(self):
        print "===> Isntalling dependency lib"
        cmd = 'yum -y install '
        item_list = self.preins_items[self.os]

        s = self._exec("lsb_release -d")
        if "Ubuntu" in s:
            self.os = 'ubuntu'
            cmd = 'apt-get -y install '
            item_list = self.preins_items[self.os]
        for lib in item_list:
            cmd = cmd + lib
            print "    >>> " + cmd
            self._exec(cmd)

    def _after_install(self):
        (lib, version) = libtag.split("-")
        path = self.install_path + self._inter("/{lib}/{version}")

        bin_list = []
        for (dirpath, dirnames, binfiles) in os.walk(self._inter("{path}/bin")):
            bin_list.extend(binfiles)
            for file in bin_list:
                cmd = self._inter("ln -s {path}/bin/{file} /usr/bin/{file}")
                os.system(cmd)

        sbin_list = []
        for (dirpath, dirnames, sbinfiles) in os.walk(self._inter("{path}/sbin")):
            sbin_list.extend(sbinfiles)
            for file in sbin_list:
                cmd = self._inter("ln -s {path}/sbin/{file} /usr/sbin/{file}")
                os.system(cmd)

        print("===> " + self.libtag + "has been installed successfuly. Detail infomation: ")



