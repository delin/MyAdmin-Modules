import re

__author__ = 'delin'

from ConfigParser import RawConfigParser
from StringIO import StringIO
from MyAdmin.functions import get_system_users


class vsFTPdParser(object):
    section = "root"
    default_config = "/etc/vsftpd.conf"
    ftp_users_file = "/etc/ftp_users.conf"
    vsftpd_version = 3.0

    default_values = {
        "anonymous_enable": "YES",
        "local_enable": "YES",
        "write_enable": "YES",
        "local_umask": "022",
        "anon_upload_enable": "YES",
        "anon_mkdir_write_enable": "YES",
        "dirmessage_enable": "YES",
        "xferlog_enable": "YES",
        "connect_from_port_20": "YES",
        "chown_uploads": "YES",
        "chown_username": "whoever",
        "xferlog_file": "/var/log/vsftpd.log",
        "xferlog_std_format": "YES",
        "idle_session_timeout": "600",
        "data_connection_timeout": "120",
        "nopriv_user": "ftpsecure",
        "async_abor_enable": "YES",
        "ascii_upload_enable": "YES",
        "ascii_download_enable": "YES",
        "ftpd_banner": "Welcome to blah FTP service.",
        "deny_email_enable": "YES",
        "banned_email_file": "/etc/vsftpd.banned_emails",
        "chroot_local_user": "YES",
        "chroot_list_enable": "YES",
        "chroot_list_file": "/etc/vsftpd.chroot_list",
        "ls_recurse_enable": "YES",
        "listen": "YES",
        "listen_ipv6": "YES",
    }

    def __init__(self, conf_path=default_config):
        conf_text = '[' + self.section + ']\n' + open(conf_path, 'r').read()
        conf_fp = StringIO(conf_text)

        self.config = RawConfigParser()
        self.config.readfp(conf_fp)

    def get(self, option):
        if self.config.has_option(self.section, option):
            return self.config.get(self.section, option)
        else:
            return None

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