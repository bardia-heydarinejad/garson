# -*- coding: utf-8 -*-
#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":

    reload(sys)
    sys.setdefaultencoding('utf8')
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "reserver.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
