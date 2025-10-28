#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

# === PARCHE TEMPORAL PARA COMPATIBILIDAD ===
import collections
import collections.abc

# Aplicar parche para marshmallow y otras librerías
collections.Mapping = collections.abc.Mapping
collections.MutableMapping = collections.abc.MutableMapping
collections.Sequence = collections.abc.Sequence
collections.MutableSequence = collections.abc.MutableSequence
collections.Set = collections.abc.Set
collections.MutableSet = collections.abc.MutableSet
collections.Iterable = collections.abc.Iterable
collections.Iterator = collections.abc.Iterator
collections.Callable = collections.abc.Callable
# === FIN DEL PARCHE ===

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FERREMAS.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()