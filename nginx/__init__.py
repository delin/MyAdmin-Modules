__author__ = 'delin'


class ModuleInit():
    def __init__(self):
        self.app_name = 'nginx'
        self.name = 'NGINX'
        self.version = 1
        self.main_page = "main"
        self.author = "Denis Yulin"
        self.author_email = "delin@delin.pro"
        self.home_page = "https://redmine.delin.pro/projects/myadmin-modules"
        self.description = "NGINX Module"
        self.in_menu = True
	self.not_installable = True


myadmin_module = ModuleInit()
