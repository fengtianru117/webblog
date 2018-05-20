#!/usr/bin/env python
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if __name__ == "__main__":
    # sys.path.append(os.path.join(BASE_DIR, ''))
    # sys.path.remove('D:\\CodeWorkSpace\\Django\\fengtianru117')
    # sys.path.pop(0)
    # print(sys.path)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fengtianru117.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
