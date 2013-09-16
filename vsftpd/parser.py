__author__ = 'delin'

import re
from ConfigParser import RawConfigParser
from StringIO import StringIO
from MyAdmin.functions import get_system_users, system_cmd, replace_in_file


class vsFTPdParser(object):
    section = "root"
    default_config = "/etc/vsftpd.conf"
    ftp_users_file = "/etc/ftp_users.conf"
    vsftpd_version = 3.0
    fd = None
    fp = None

    default_values = {
        "anonymous_enable": {
            "default": "YES",
            "re": "^YES$|^NO$",
        },
        "local_enable": {
            "default": "YES",
            "re": "^YES$|^NO$",
        },
        "write_enable": {
            "default": "YES",
            "re": "^YES$|^NO$",
        },
        "local_umask": {
            "default": "022",
            "re": "[0-7]{3}",
        },
        "anon_upload_enable": {
            "default": "YES",
            "re": "^YES$|^NO$",
        },
        "anon_mkdir_write_enable": {
            "default": "YES",
            "re": "^YES$|^NO$",
        },
        "dirmessage_enable": {
            "default": "YES",
            "re": "^YES$|^NO$",
        },
        "xferlog_enable": {
            "default": "YES",
            "re": "^YES$|^NO$",
        },
        "connect_from_port_20": {
            "default": "YES",
            "re": "^YES$|^NO$",
        },
        "chown_uploads": {
            "default": "YES",
            "re": "^YES$|^NO$",
        },
        "chown_username": {
            "default": "whoever",
            "re": "[\w]{1,128}",
        },
        "xferlog_file": {
            "default": "/var/log/vsftpd.log",
            "re": "^[\W+\/\\\]{1,}",
        },
        "xferlog_std_format": {
            "default": "YES",
            "type": "bool",
            "re": "^YES$|^NO$",
        },
        "idle_session_timeout": {
            "default": "600",
            "re": "[\d+]{1,6}",
        },
        "data_connection_timeout": {
            "default": "120",
            "re": "[\d+]{1,6}",
        },
        "nopriv_user": {
            "default": "ftpsecure",
            "re": "[\w]{1,128}",
        },
        "async_abor_enable": {
            "default": "YES",
            "re": "^YES$|^NO$",
        },
        "ascii_upload_enable": {
            "default": "YES",
            "re": "^YES$|^NO$",
        },
        "ascii_download_enable": {
            "default": "YES",
            "re": "^YES$|^NO$",
        },
        "ftpd_banner": {
            "default": "Welcome to blah FTP service.",
            "re": "[\S+]{0,}",
        },
        "deny_email_enable": {
            "default": "YES",
            "re": "^YES$|^NO$",
        },
        "banned_email_file": {
            "default": "/etc/vsftpd.banned_emails",
            "re": "^[\W+\/\\\]{1,}",
        },
        "chroot_local_user": {
            "default": "YES",
            "re": "^YES$|^NO$",
        },
        "chroot_list_enable": {
            "default": "YES",
            "re": "^YES$|^NO$",
        },
        "chroot_list_file": {
            "default": "/etc/vsftpd.chroot_list",
            "re": "^[\W+\/\\\]{1,}",
        },
        "ls_recurse_enable": {
            "default": "YES",
            "re": "^YES$|^NO$",
        },
        "listen": {
            "default": "YES",
            "re": "^YES$|^NO$",
        },
        "listen_ipv6": {
            "default": "YES",
            "re": "^YES$|^NO$",
        },
    }

    def __init__(self, conf_path=default_config):
        conf_text = '[' + self.section + ']\n' + open(conf_path, 'rw').read()
        self.fp = StringIO(conf_text)
        # self.fp = open(conf_path, 'rw')

        self.config = RawConfigParser()
        self.config.readfp(self.fp)

    def check_value(self, option, value):
        if re.match(self.default_values[option]['re'], value):
            return True
        return False

    def get_default_value(self, option):
        value = self.default_values[option]['default'].copy() or None
        return value

    def get(self, option):
        if self.config.has_option(self.section, option):
            return self.config.get(self.section, option)
        return None

    def set(self, option, value):
        if self.check_value(option, value):
            self.config.set(self.section, option, value)
            return True
        return False

    def options(self):
        return self.config.options(self.section)

    def get_ftp_users(self):
        system_users = get_system_users()

        try:
            ftp_users_fd = open(self.ftp_users_file, "r")
        except:
            raise

        no_ftp_users = []
        for user in ftp_users_fd:
            no_ftp_users.append(re.sub("^\s+|\n|\r|\s+$", '', user))

        ftp_users = []
        for user in system_users:
            if user['name'] not in no_ftp_users and user['uid'] >= 1000:
                ftp_users.append(user)

        return ftp_users

    def get_configs_array(self):
        configs = self.default_values.copy()

        for option in configs:
            configs[option] = {
                "value": self.get(option),
                "default": self.default_values[option]['default'] or None,
            }
        return configs

    def write(self):
        items = self.config.items(self.section)
        for (key, value) in items:
            grep_string = "grep '^%s=*' %s" % (key, self.default_config)
            if system_cmd(grep_string) == 0:
                print "replace", key, value
                replace_in_file(self.default_config, r"%s=(.*)" % key, '%s=%s' % (key, value))
            else:
                add_string = "echo '%s=%s' >> %s" % (key, value, self.default_config)
                system_cmd(add_string)