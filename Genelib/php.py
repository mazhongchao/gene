#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import urllib2
import hashlib
import dna

class PHP(dna.DNA):
    libtag = "php-7.2.6"
    url = "http://cn.php.net/distributions/php-7.2.6.tar.gz"
    desc = "General-purpose scripting language"
    homepage = "https://secure.php.net/"
    sha256 = "a9f30daf6af82ac02e692465cfd65b04a60d56106c961926e264d2621d313f0e"
    preins_items = {"centos":["openssl-devel.x86_64", "bzip2-devel.x86_64", "libcurl-devel.x86_64",
                    "libpng-devel.x86_64", "freetype-devel.x86_64", "libjpeg-turbo-devel.x86_64",
                    "libmcrypt-devel.x86_64", "unixODBC-devel.x86_64", "unixODBC.x86_64", "libxml2-devel"],
                    "ubuntu":["libxml2-dev", "libssl-dev", "libcurl4-openssl-dev", "libbz2-dev",
                    "libjpeg-dev", "libpng-dev", "mcrypt-dev", "libfreetype6-dev", "unixodbc unixodec-dev"]
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

        print("\033[1;37m===>\033[0m Installing " + self.libtag)
        download_path = self.download_path

        os.system(self._inter("cd {download_path}"))
        os.system(self._inter("tar xzf {libtag}.tar.gz"))
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

        print "\033[1;37m===>\033[0m Downloading " + libtag + " from " + self.url
        f = urllib2.urlopen(self.url)
        with open(self._inter("{download_path}/{libtag}.tar.gz", "wb")) as code:
            code.write(f.read())

    def file_verify(self):
        libtag = self.libtag
        download_path = self.download_path
        BUF_SIZE = 65536
        print "\033[1;37m===>\033[0m Verfiying"
        with open(self._inter("{download_path}/{libtag}.tar.gz", "rb")) as f:
            while True:
                data = f.read(BUF_SIZE)
                if not data:
                    break

                if hashlib.sha256(data) == self.sha256:
                    return True
                else:
                    print "\033[1;37m===>\033[0m Verify file " + self.libtag + ".tar.gz faild for " + hashlib.sha256(data)
                    return False
        return False

    def _before_install(self):
        print "\033[1;37m===>\033[0m Isntalling dependency lib:"
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
                cmd = self._inter("ln -s {path}/bin/{file} /usr/local/bin/{file}")
                os.system(cmd)

        sbin_list = []
        for (dirpath, dirnames, sbinfiles) in os.walk(self._inter("{path}/sbin")):
            sbin_list.extend(sbinfiles)
            for file in sbin_list:
                cmd = self._inter("ln -s {path}/sbin/{file} /usr/local/sbin/{file}")
                os.system(cmd)

        self._set_starup()
        self._install_detail()

    def _set_starup(self):
        if self.os == "centos":
            cmd = "cp /usr/local/src/gene_downdloads/{libtag}/sapi/fpm/php-fpm.service /usr/lib/systemd/system"
            os.system(cmd)
            # cmd = "ln -s /usr/lib/systemd/system/php-fpm.service /etc/systemd/system/multi-user.target.wants/php-fpm.serivce"
            # os.system(cmd)

        if self.os == "ubuntu":
            cmd = "cp /usr/local/src/gene_downdloads/{libtag}/sapi/fpm/init.d.php-fpm /etc/init.d/php-fpm.service"
            os.system(cmd)
            cmd = "chmod 755 /etc/init.d/php-fpm.serivce"
            os.system(cmd)

    def _install_detail(self):
        libtag = self.libtag
        (lib, version) = libtag.split("-")
        config_path = self.base_path + self._inter("/etc/{lib}/") + version[0:3]
        print("\033[1;32m===>\033[0m " + self.libtag + " has been installed successfuly. Detail infomation: ")
        ss = """
              Installed Path: /usr/local/opt/{libtag}
            Config File Path: /usr/local/etc/{config_path}
             Startup Service: /usr/lib/systemd/system/php-fpm.service (for CentOS)
                              /etc/init.d/php-fpm.serivce (for Ubuntu)

            To start php-fpm:
                sudo systemctl start php-fpm.service(for CentOS)
                /etc/init.d/php-fpm.serivce start(for Ubuntu)

            Or, just run: php-fpm & (be sure that path '/usr/local/sbin' in $PATH)

            If you want to start php-fpm automatically as a background service, just run:
                sudo systemctl enable php-fpm.service(for CentOS)
                sudo update-rc.d test defaults 95(for Ubuntu)
        """
        print ss

    def echo(self):
        print "Test....PHP"

