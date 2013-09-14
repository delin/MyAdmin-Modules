from django.db import models
from django.utils.translation import ugettext as _


class Setting(models.Model):
    name = models.CharField(verbose_name=_("Name"), max_length=32, unique=True)
    value = models.CharField(verbose_name=_("Value"), max_length=1024)


class User(models.Model):
    name = models.CharField(verbose_name=_("Username"), max_length=64, unique=True)
    uid = models.PositiveSmallIntegerField(verbose_name=_("UID"), unique=True)
    home = models.FilePathField(verbose_name=_("Home dir"), allow_files=False, allow_folders=True)
    shell = models.FilePathField(verbose_name=_("Shell"), allow_files=True, allow_folders=False)


class Group(models.Model):
    name = models.CharField(verbose_name=_("Group name"), max_length=64, unique=True)
    gid = models.PositiveSmallIntegerField(verbose_name=_("GID"), unique=True)
    members = models.ManyToManyField(User, verbose_name=_("Members"))