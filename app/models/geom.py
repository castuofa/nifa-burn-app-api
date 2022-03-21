import geojson

from shapely.geometry import asShape
from geoalchemy2.elements import WKBElement
from geoalchemy2.shape import to_shape
from ormar.exceptions import ModelDefinitionError
from ormar.fields.base import BaseField
from ormar.fields.model_fields import ModelFieldFactory
from geoalchemy2 import Geometry
from geoalchemy2 import func
from typing import Any


def ewkb_to_wkt(geom: WKBElement):
    """
    Converts a geometry formated as WKBE to WKT
    in order to parse it into pydantic Model

    Args:
        geom (WKBElement): A geometry from GeoAlchemy query
    """
    return to_shape(geom).wkt



class GeometryType(str):
    """
    Custom type for geometry validations from PostGIS
    """

    @classmethod
    def __get_validators__(cls):
        # one or more validators may be yielded which will be called in the
        # order to validate the input, each validator will receive as an input
        # the value returned from the previous validator
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if isinstance(v, WKBElement):
            return ewkb_to_wkt(v)
        if isinstance(v, str):
            return v
        raise ValueError('must be a valid WKBE element')

    def __repr__(self):
        return f'Geometry({super().__repr__()})'

    @classmethod
    def from_geojson(cls, geojson_str: str):
        return to_shape(asShape(geojson.loads(geojson_str)))


class GeoJSONGeometryType(str):
    @classmethod
    def __get_validators__(cls):
        # one or more validators may be yielded which will be called in the
        # order to validate the input, each validator will receive as an input
        # the value returned from the previous validator
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if isinstance(v, str):
            return geojson.loads(v)
        if isinstance(v, dict):
            return v
        raise ValueError('must be valid GeoJSON')

    def __repr__(self):
        return geojson.dumps(self)


class OrmarGeometry(ModelFieldFactory, Geometry):

    """
    Geometry field factory that construct Field classes and populated their values.
    """

    _type = GeometryType
    _sample = "POLYGON((0 0,1 0,1 1,0 1,0 0))"
    _accepted_shapes = [
        "GEOMETRY",
        "POINT",
        "LINESTRING",
        "POLYGON",
        "MULTIPOINT",
        "MULTILINESTRING",
        "MULTIPOLYGON",
        "GEOMETRYCOLLECTION",
        "CURVE",
    ]

    def __new__(  # type: ignore
        cls, *, shape: str = None, srid: int = None, **kwargs: Any
    ) -> BaseField:
        kwargs = {
            **kwargs,
            **{
                k: v
                for k, v in locals().items()
                if k not in ["cls", "__class__", "kwargs"]
            },
        }
        return super().__new__(cls, **kwargs)

    @classmethod
    def get_column_type(cls, **kwargs: Any) -> Geometry:
        """
        Return proper type of db column for given field type.
        Accepts required and optional parameters that each column type accepts.
        :param kwargs: key, value pairs of sqlalchemy options
        :type kwargs: Any
        :return: initialized column with proper options
        :rtype: sqlalchemy Column
        """
        shape = kwargs.pop("shape")

        nullable = kwargs.pop("sql_nullable", False)
        kwargs["nullable"] = nullable

        return Geometry(shape, **kwargs)

    @classmethod
    def validate(cls, **kwargs: Any) -> None:  # pragma no cover
        """
        Used to validate if all required parameters on a given field type are set.
        :param kwargs: all params passed during construction
        :type kwargs: Any
        """
        shape = kwargs.get("shape", None)
        if not shape and shape not in cls._accepted_shapes:
            raise ModelDefinitionError(f"Shape must be one of {cls._accepted_shapes}")


class GeometryGeoJSON(Geometry):

    from_text = 'ST_GeomFromGeoJSON'
    as_binary = 'ST_AsGeoJSON'
    ElementType = dict

    # Sourced from: https://stackoverflow.com/questions/24034007/correct-json-format-to-save-into-geoalchemy2-geometry-field
    def result_processor(self, dialect, coltype):
        # Postgres will give us JSON, thanks to `ST_AsGeoJSON()`. We just return it.
        def process(value):
            return value
        return process

    def bind_expression(self, bindvalue):
        return func.ST_SetSRID(super().bind_expression(bindvalue), self.srid)

    def bind_processor(self, dialect):
        # Dump incoming values as JSON
        def process(bindvalue):
            if bindvalue is None:
                return None
            else:
                return geojson.dumps(bindvalue)
        return process

    @property
    def python_type(self):
        return dict


class OrmarGeoJSON(OrmarGeometry):

    _type = GeoJSONGeometryType

    @classmethod
    def get_column_type(cls, **kwargs: Any) -> Geometry:
        """
        Return proper type of db column for given field type.
        Accepts required and optional parameters that each column type accepts.
        :param kwargs: key, value pairs of sqlalchemy options
        :type kwargs: Any
        :return: initialized column with proper options
        :rtype: sqlalchemy Column
        """
        shape = kwargs.pop("shape")

        nullable = kwargs.pop("sql_nullable", False)
        kwargs["nullable"] = nullable

        return GeometryGeoJSON(shape, **kwargs)