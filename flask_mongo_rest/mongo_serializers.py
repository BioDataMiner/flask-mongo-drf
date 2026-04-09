# mongo_serializers.py
from bson import ObjectId
from datetime import datetime
from collections import OrderedDict
from typing import Any, Dict, List, Callable

from .mongo_exceptions import ValidationError


class Field:
    """字段基类"""

    def __init__(
            self,
            required: bool = False,
            default: Any = None,
            allow_null: bool = False,
            read_only: bool = False,
            write_only: bool = False,
            validators: List[Callable] = None,
            help_text: str = "",
    ):
        self.required = required
        self.default = default
        self.allow_null = allow_null
        self.read_only = read_only
        self.write_only = write_only
        self.validators = validators or []
        self.help_text = help_text
        self.field_name = None  # 由 Serializer 元类设置

    def to_representation(self, value: Any) -> Any:
        """序列化：将内部值转换为输出格式"""
        if value is None:
            return None
        return value

    def to_internal_value(self, value: Any) -> Any:
        """反序列化：将输入值转换为内部存储格式"""
        if value is None:
            if self.required:
                raise ValidationError(f"{self.field_name} is required.")
            return self.default
        return value

    def validate(self, value: Any) -> Any:
        """自定义校验，子类可重写"""
        for v in self.validators:
            v(value)
        return value


class CharField(Field):
    def __init__(self, max_length: int = None, min_length: int = None, **kwargs):
        super().__init__(**kwargs)
        self.max_length = max_length
        self.min_length = min_length

    def to_internal_value(self, value: Any) -> str:
        value = super().to_internal_value(value)
        if value is None:
            return None
        if not isinstance(value, str):
            value = str(value)
        if self.min_length is not None and len(value) < self.min_length:
            raise ValidationError(f"{self.field_name} length must be >= {self.min_length}")
        if self.max_length is not None and len(value) > self.max_length:
            raise ValidationError(f"{self.field_name} length must be <= {self.max_length}")
        return value


class IntegerField(Field):
    def __init__(self, min_value: int = None, max_value: int = None, **kwargs):
        super().__init__(**kwargs)
        self.min_value = min_value
        self.max_value = max_value

    def to_internal_value(self, value: Any) -> int:
        value = super().to_internal_value(value)
        if value is None:
            return None
        try:
            value = int(value)
        except (TypeError, ValueError):
            raise ValidationError(f"{self.field_name} must be an integer.")
        if self.min_value is not None and value < self.min_value:
            raise ValidationError(f"{self.field_name} must be >= {self.min_value}")
        if self.max_value is not None and value > self.max_value:
            raise ValidationError(f"{self.field_name} must be <= {self.max_value}")
        return value


class FloatField(Field):
    def to_internal_value(self, value: Any) -> float:
        value = super().to_internal_value(value)
        if value is None:
            return None
        try:
            return float(value)
        except (TypeError, ValueError):
            raise ValidationError(f"{self.field_name} must be a number.")


class BooleanField(Field):
    def to_internal_value(self, value: Any) -> bool:
        value = super().to_internal_value(value)
        if value is None:
            return None
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() in ('true', '1', 'yes', 'on')
        return bool(value)


class DateTimeField(Field):
    def __init__(self, format: str = "%Y-%m-%d %H:%M:%S", **kwargs):
        super().__init__(**kwargs)
        self.format = format

    def to_representation(self, value: Any) -> str:
        if isinstance(value, datetime):
            return value.strftime(self.format)
        return value

    def to_internal_value(self, value: Any) -> datetime:
        value = super().to_internal_value(value)
        if value is None:
            return None
        if isinstance(value, datetime):
            return value
        try:
            return datetime.strptime(value, self.format)
        except (TypeError, ValueError):
            raise ValidationError(f"{self.field_name} must be datetime string with format {self.format}")


class ObjectIdField(Field):
    def to_representation(self, value: Any) -> str:
        if isinstance(value, ObjectId):
            return str(value)
        return value

    def to_internal_value(self, value: Any) -> ObjectId:
        value = super().to_internal_value(value)
        if value is None:
            return None
        if isinstance(value, ObjectId):
            return value
        if ObjectId.is_valid(str(value)):
            return ObjectId(str(value))
        raise ValidationError(f"{self.field_name} is not a valid ObjectId.")


class ListField(Field):
    def __init__(self, child: Field = None, **kwargs):
        super().__init__(**kwargs)
        self.child = child or CharField()

    def to_representation(self, value: Any) -> List:
        if not isinstance(value, list):
            return []
        return [self.child.to_representation(item) for item in value]

    def to_internal_value(self, value: Any) -> List:
        value = super().to_internal_value(value)
        if value is None:
            return []
        if not isinstance(value, list):
            raise ValidationError(f"{self.field_name} must be a list.")
        return [self.child.to_internal_value(item) for item in value]


class DictField(Field):
    def to_representation(self, value: Any) -> Dict:
        if not isinstance(value, dict):
            return {}
        return value

    def to_internal_value(self, value: Any) -> Dict:
        value = super().to_internal_value(value)
        if value is None:
            return {}
        if not isinstance(value, dict):
            raise ValidationError(f"{self.field_name} must be a dict.")
        return value


class SerializerMetaclass(type):
    def __new__(mcs, name, bases, attrs):
        fields = OrderedDict()
        for base in bases:
            if hasattr(base, '_fields'):
                fields.update(base._fields)
        for key, value in attrs.items():
            if isinstance(value, Field):
                value.field_name = key
                fields[key] = value
        attrs['_fields'] = fields
        return super().__new__(mcs, name, bases, attrs)


class Serializer(metaclass=SerializerMetaclass):
    def __init__(self, instance=None, data=None, partial=False):
        self.instance = instance
        self.initial_data = data
        self.partial = partial
        self._validated_data = None
        self._errors = None

    @property
    def errors(self):
        return self._errors

    @property
    def validated_data(self):
        if self._errors:
            raise ValidationError(self._errors)
        return self._validated_data

    def is_valid(self, raise_exception=False):
        self._errors = {}
        self._validated_data = {}
        if self.initial_data is None:
            self._errors['non_field_errors'] = ['No data provided']
            return False

        for field_name, field in self._fields.items():
            if field.read_only:
                continue
            value = self.initial_data.get(field_name)
            if value is None and not field.allow_null:
                if field.required and not self.partial:
                    self._errors[field_name] = ['This field is required.']
                    continue
                if field.default is not None:
                    value = field.default
                else:
                    if self.partial and field_name in self.initial_data:
                        # partial update 且显式传了 None，允许
                        pass
                    else:
                        continue
            try:
                internal = field.to_internal_value(value)
                internal = field.validate(internal)
                self._validated_data[field_name] = internal
            except ValidationError as e:
                self._errors[field_name] = str(e)

        if self._errors:
            if raise_exception:
                raise ValidationError(self._errors)
            return False
        return True

    def save(self, **kwargs):
        if self.instance is not None:
            # 更新
            for key, value in self.validated_data.items():
                setattr(self.instance, key, value)
            # 这里需要调用 model 的 update 方法，由 ViewSet 处理
            return self.instance
        else:
            # 创建
            return self.validated_data

    def data(self):
        if self.instance is not None:
            return self.to_representation(self.instance)
        return self.to_representation(self.validated_data)

    def to_representation(self, obj):
        ret = OrderedDict()
        for field_name, field in self._fields.items():
            if field.write_only:
                continue
            value = getattr(obj, field_name, None) if hasattr(obj, field_name) else obj.get(field_name)
            ret[field_name] = field.to_representation(value)
        return ret

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        return instance

    def create(self, validated_data):
        return validated_data


class ModelSerializer(Serializer):
    def __init__(self, instance=None, data=None, partial=False, model=None):
        self.model = model
        super().__init__(instance, data, partial)

    def to_representation(self, obj):
        # obj 可以是 dict 或 MongoBaseModel 实例
        ret = OrderedDict()
        for field_name, field in self._fields.items():
            if field.write_only:
                continue
            if isinstance(obj, dict):
                value = obj.get(field_name)
            else:
                value = getattr(obj, field_name, None)
            ret[field_name] = field.to_representation(value)
        return ret

    def create(self, validated_data):
        # 返回 dict，由 Model 层插入
        return validated_data

    def update(self, instance, validated_data):
        # instance 是 dict 或 model 实例
        instance.update(validated_data)
        return instance
