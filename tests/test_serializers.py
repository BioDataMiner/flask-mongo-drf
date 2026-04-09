import pytest
from datetime import datetime
from bson import ObjectId

from flask_mongo_drf.mongo_exceptions import ValidationError
from flask_mongo_drf.mongo_serializers import (
    Serializer,
    CharField,
    IntegerField,
    FloatField,
    BooleanField,
    DateTimeField,
    ObjectIdField,
    ListField,
    DictField,
)


class UserSerializer(Serializer):
    name = CharField(required=True, min_length=2)
    age = IntegerField(min_value=0)


def test_serializer_valid():
    data = {"name": "Tom", "age": 20}
    s = UserSerializer(data=data)
    assert s.is_valid()
    assert s.validated_data["name"] == "Tom"
    assert s.validated_data["age"] == 20


def test_serializer_invalid():
    data = {"name": "T"}  # 长度不足
    s = UserSerializer(data=data)
    assert not s.is_valid()
    assert "name" in s.errors


def test_serializer_partial():
    data = {"age": 30}
    s = UserSerializer(data=data, partial=True)
    assert s.is_valid()


def test_charfield_max_length():
    class S(Serializer):
        name = CharField(max_length=5)

    s = S(data={"name": "123456"})
    assert not s.is_valid()
    assert "name" in s.errors


def test_integerfield_validation():
    class S(Serializer):
        age = IntegerField(min_value=18, max_value=99)

    assert S(data={"age": 20}).is_valid() is True
    assert S(data={"age": 10}).is_valid() is False
    assert S(data={"age": 100}).is_valid() is False
    assert S(data={"age": "abc"}).is_valid() is False


def test_floatfield():
    class S(Serializer):
        score = FloatField()

    s = S(data={"score": 95.5})
    assert s.is_valid()
    assert s.validated_data["score"] == 95.5

    s = S(data={"score": "not_float"})
    assert not s.is_valid()


def test_booleanfield():
    class S(Serializer):
        active = BooleanField()

    # 修复：必须先调用 is_valid()
    s1 = S(data={"active": True})
    assert s1.is_valid()
    assert s1.validated_data["active"] is True

    s2 = S(data={"active": "true"})
    assert s2.is_valid()
    assert s2.validated_data["active"] is True

    s3 = S(data={"active": "false"})
    assert s3.is_valid()
    assert s3.validated_data["active"] is False


def test_datetimefield():
    class S(Serializer):
        created_at = DateTimeField(format="%Y-%m-%d %H:%M:%S")

    valid_data = {"created_at": "2025-01-01 12:00:00"}
    s = S(data=valid_data)
    assert s.is_valid()
    assert isinstance(s.validated_data["created_at"], datetime)

    invalid_data = {"created_at": "2025-01-01"}
    s2 = S(data=invalid_data)
    assert not s2.is_valid()


def test_objectidfield():
    class S(Serializer):
        _id = ObjectIdField()

    oid = ObjectId()
    s = S(data={"_id": str(oid)})
    assert s.is_valid()
    assert isinstance(s.validated_data["_id"], ObjectId)

    s2 = S(data={"_id": "invalid_id"})
    assert not s2.is_valid()


def test_listfield():
    class S(Serializer):
        tags = ListField(child=CharField())

    s = S(data={"tags": ["a", "b", "c"]})
    assert s.is_valid()
    assert s.validated_data["tags"] == ["a", "b", "c"]

    s2 = S(data={"tags": "not_list"})
    assert not s2.is_valid()


def test_dictfield():
    class S(Serializer):
        info = DictField()

    s = S(data={"info": {"key": "value"}})
    assert s.is_valid()

    s2 = S(data={"info": 123})
    assert not s2.is_valid()


def test_allow_null():
    class S(Serializer):
        name = CharField(allow_null=True)

    s = S(data={"name": None})
    assert s.is_valid()


def test_required_field():
    class S(Serializer):
        name = CharField(required=True)

    s = S(data={})
    assert not s.is_valid()
    assert "name" in s.errors


def test_serializer_to_representation():
    class S(Serializer):
        name = CharField()
        age = IntegerField()

    obj = {"name": "Alice", "age": 25}
    s = S(instance=obj)
    output = s.data()
    assert output["name"] == "Alice"
    assert output["age"] == 25


def test_validate_raise_exception():
    class S(Serializer):
        name = CharField(required=True)

    s = S(data={})
    with pytest.raises(ValidationError):
        s.is_valid(raise_exception=True)
