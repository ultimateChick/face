# coding=utf-8
from django.db import models

import os
import random

# Create your models here.


class Picture(models.Model):
    # path = models.TextField(verbose_name=u"文件路径")
    filename = models.CharField(verbose_name=u"文件名", max_length=255)

    def get_avatar(self):
        return "/media/img/%s" % self.filename

    @staticmethod
    def get_avail_path(dir_local, dir_relative, name):
        path = dir_relative + name
        while os.path.exists(dir_local + path):
            name = str(hash(''.join(random.sample('qwertyuioplkjhgfdsazxcvbnm1234567890', 10)))) + name
            path = dir_relative + name
        return path, name

    def avatar_file_save(self, f):
        if not self.avatar_type_switch:
            self.avatar_type_switch = True
        path, name = Picture.get_avail_path(os.path.dirname(os.path.dirname(__file__)).replace('\\', '/') + '/',
                                            'media/img/', f.name)
        try:
            dest = open(os.path.dirname(os.path.dirname(__file__)).replace('\\', '/') + '/' + path, 'wb+')
        except IOError:
            os.makedirs('media//img')
            dest = open(os.path.dirname(os.path.dirname(__file__)).replace('\\', '/') + '/' + path, 'wb+')
        for chunk in f.chunks():
            dest.write(chunk)
        dest.close()

        return "/media/img/%s" % self.avatar