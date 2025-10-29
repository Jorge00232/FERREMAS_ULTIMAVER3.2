# ferreteria/patches.py
"""
Parche temporal para compatibilidad con Python 3.11+
Soluciona el error: cannot import name 'Mapping' from 'collections'
"""
import collections
import collections.abc

# Parche COMPLETO para marshmallow y otras librerías desactualizadas
if not hasattr(collections, 'Mapping'):
    collections.Mapping = collections.abc.Mapping

if not hasattr(collections, 'MutableMapping'):
    collections.MutableMapping = collections.abc.MutableMapping

if not hasattr(collections, 'Sequence'):
    collections.Sequence = collections.abc.Sequence

if not hasattr(collections, 'MutableSequence'):
    collections.MutableSequence = collections.abc.MutableSequence

if not hasattr(collections, 'Set'):
    collections.Set = collections.abc.Set

if not hasattr(collections, 'MutableSet'):
    collections.MutableSet = collections.abc.MutableSet

if not hasattr(collections, 'Iterable'):
    collections.Iterable = collections.abc.Iterable

if not hasattr(collections, 'Iterator'):
    collections.Iterator = collections.abc.Iterator

if not hasattr(collections, 'KeysView'):
    collections.KeysView = collections.abc.KeysView

if not hasattr(collections, 'ItemsView'):
    collections.ItemsView = collections.abc.ItemsView

if not hasattr(collections, 'ValuesView'):
    collections.ValuesView = collections.abc.ValuesView

print("✅ Parche de compatibilidad Python 3.11+ aplicado correctamente")