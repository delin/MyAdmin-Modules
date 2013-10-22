from system_tools.users import SystemUsers

__author__ = 'delin'

import re
from ConfigParser import RawConfigParser
from StringIO import StringIO
from MyAdmin.functions import system_cmd, replace_in_file


class vsFTPdParser(object):
    section = "root"
    default_config = "/etc/vsftpd.conf"
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
        "check_shell": {
            "default": "YES",
            "re": "^YES$|^NO$",
        },
        "userlist_enable": {
            "default": "NO",
            "re": "^YES$|^NO$",
        },
        "userlist_deny": {
            "default": "YES",
            "re": "^YES$|^NO$",
        },
        "userlist_file": {
            "default": "/etc/ftpusers",
            "re": "^[\W+\/\\\]{1,}",
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
        user_management = SystemUsers()
        system_users = user_management.get_users()

        if self.get('userlist_enable') == 'YES':
            userlist_enable = True
        else:
            userlist_enable = False

        if self.get('userlist_deny') == 'YES':
            userlist_deny = True
        else:
            userlist_deny = False

        if self.get('check_shell') == 'YES':
            check_shell = True
        else:
            check_shell = False

        ftpusers_file = self.get('userlist_file')
        ftpusers_access_list = []
        ftpusers_deny_list = []

        if userlist_enable:
            try:
                ftpusers_list_fd = open(ftpusers_file, 'r')

                for user in ftpusers_list_fd:
                    if not re.match('(^#|^$)', user):
                        cur_user = re.sub("^\s+|\n|\r|\s+$", '', user)
                        if userlist_deny:
                            ftpusers_deny_list.append(cur_user)
                        else:
                            ftpusers_access_list.append(cur_user)
            except BaseException as e:
                print "[debug]: " + str(e)

        allowed_shells = []
        try:
            allowed_shells_fd = open('/etc/shells', 'r')
            for shell in allowed_shells_fd:
                if not re.match('(^#|^$)', shell):
                    cur_shell = re.sub("^\s+|\n|\r|\s+$", '', shell)
                    allowed_shells.append(cur_shell)
        except BaseException as e:
            print "[debug]: " + str(e)

        ftp_users = []
        for user in system_users:
            if check_shell:
                if user['shell'] not in allowed_shells:
                    continue

            if userlist_deny:
                if user['name'] in ftpusers_deny_list:
                    continue
            else:
                if user['name'] not in ftpusers_access_list:
                    continue

            if user['uid'] >= 1000:
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