__author__ = 'delin'


class ModuleInit():
    def __init__(self):
        self.app_name = 'vsftpd'
        self.name = 'vsFTPd'
        self.version = 1
        self.main_page = "main"
        self.author = "Denis Yulin"
        self.author_email = "delin@delin.pro"
        self.home_page = "https://redmine.delin.pro/projects/myadmin-modules"
        self.description = "vsFTPd Module"
        self.in_menu = True


myadmin_module = ModuleInit()
