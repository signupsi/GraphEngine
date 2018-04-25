from .type_sys import TSLStruct, TSLCell
from .type_spec import TSLTypeSpec, PrimitiveSpec, ListSpec, CellSpec, StructSpec
from Redy.Magic.Pattern import Pattern
from Redy.Magic.Classic import const_return
import typing


# noinspection PyTypeChecker
@Pattern
def type_map_spec(py_type) -> TSLTypeSpec:
    # noinspection PyUnresolvedReferences,PyProtectedMember
    if issubclass(py_type, typing.List):
        return list
    elif issubclass(py_type, (TSLCell, TSLStruct)):
        return TSLStruct
    elif isinstance(py_type, typing._ForwardRef):
        return py_type.__forward_arg__
    return py_type


@type_map_spec.match(int)
@const_return
def type_map_spec(_):
    return PrimitiveSpec("int", int)


@type_map_spec.match(str)
@const_return
def type_map_spec(_):
    return PrimitiveSpec('string', str)


@type_map_spec.match(float)
@const_return
def type_map_spec(_):
    return PrimitiveSpec("double", float)


def _generic_type_map(typ_tuple):
    if not isinstance(typ_tuple, tuple):
        return type_map_spec(typ_tuple)

    # only work for list generic
    return ListSpec(_generic_type_map(typ_tuple[1]))


@type_map_spec.match(list)
def type_map_spec(typ: typing.List):
    # noinspection PyUnresolvedReferences
    trees = typ._subs_tree()
    if not isinstance(trees, tuple):
        raise TypeError("List without type params")
    return _generic_type_map(trees)


@type_map_spec.match(TSLStruct)
def type_map_spec(typ: TSLStruct):
    return typ.get_spec()
