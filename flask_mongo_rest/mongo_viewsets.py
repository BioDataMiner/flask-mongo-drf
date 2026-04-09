# mongo_viewset.py
from bson import ObjectId
from functools import wraps
from flasgger import swag_from
from flask import request, Blueprint
from typing import Type, Any, Dict, List, Optional

from .mongo_filters import FilterSet
from .mongo_models import MongoBaseModel
from .mongo_responses import custom_response
from .mongo_paginations import MongoPagination
from .mongo_decorators import handle_api_errors
from .mongo_swagger import generate_swagger_config
from .mongo_exceptions import NotFound, ValidationError
from .mongo_serializers import Serializer, ModelSerializer


class MongoModelViewSet:
    """
    DRF 风格的 ModelViewSet，提供 list, create, retrieve, update, partial_update, destroy。

    子类需要配置：
    - collection: PyMongo Collection 实例（必须）
    - serializer_class: 序列化器类（可选，默认自动生成）
    - filterset_class: 过滤器类（可选）
    - pagination_class: 分页器类（默认 MongoPagination）
    - default_sort_by / default_sort_order: 默认排序
    """
    model_class = None  # 模型类（推荐）
    collection = None  # 直接传入 Collection 对象（备选）
    serializer_class: Type[Serializer] = None
    filterset_class: Optional[Type[FilterSet]] = None
    pagination_class: Optional[Type[MongoPagination]] = MongoPagination
    default_sort_by: str = "_id"
    default_sort_order: int = -1

    def __init__(self):
        # 1. 获取模型实例
        if self.model_class is not None:
            self.model = self.model_class()  # 实例化模型，模型内部已绑定 collection
        elif self.collection is not None:
            self.model = MongoBaseModel(self.collection)
        else:
            raise ValueError("Either model_class or collection must be provided")

        # 2. 确定序列化器
        self._serializer_class = self.serializer_class or self._get_default_serializer()

    def _get_default_serializer(self):
        """如果没有指定 serializer_class，动态创建一个 ModelSerializer"""

        # 简单实现：可以扫描 collection 的一条文档来推断字段（可选）
        # 这里返回一个空的 ModelSerializer，实际使用时需要用户指定或增强
        class AutoSerializer(ModelSerializer):
            class Meta:
                model = None  # 需要用户显式定义或传入

        return AutoSerializer

    def get_serializer(self, instance=None, data=None, partial=False):
        """获取序列化器实例"""
        return self._serializer_class(instance=instance, data=data, partial=partial)

    def get_filter_dict(self) -> Dict[str, Any]:
        """从 request args 构建 MongoDB 过滤条件"""
        if self.filterset_class:
            return self.filterset_class(data=request.args.to_dict()).get_query_dict()
        return {}

    def get_pipeline(self, filter_dict: Dict[str, Any]) -> Optional[List[Dict[str, Any]]]:
        """
        子类可重写，返回聚合管道。
        若返回非 None，则使用聚合管道查询（忽略排序和普通过滤）。
        """
        return None

    def _apply_pagination(self, cursor, total):
        """对游标应用分页，返回 (结果列表, 分页元数据)"""
        if self.pagination_class:
            paginator = self.pagination_class(request.args, total, request.endpoint)
            cursor = cursor.skip(paginator.skip).limit(paginator.limit)
            return list(cursor), paginator.get_meta()
        return list(cursor), {}

    def _handle_normal_list(self, filter_dict):
        """处理非聚合的列表查询"""
        total = self.model.count_documents(filter_dict)
        cursor = self.model.find_all(filter_dict, self.default_sort_by, self.default_sort_order)
        results, meta = self._apply_pagination(cursor, total)
        serializer = self.get_serializer()
        serialized_data = [serializer.to_representation(doc) for doc in results]
        return custom_response(data=serialized_data, total=total, **meta)

    def _handle_aggregate_list(self, filter_dict, pipeline):
        """处理聚合管道的列表查询（使用 $facet 同时获取数据和总数）"""
        # 构建 facet 管道
        facet_pipeline = pipeline + [{
            "$facet": {
                "data": [],
                "total": [{"$count": "count"}]
            }
        }]
        agg_result = list(self.model.aggregate(facet_pipeline))
        total = agg_result[0]['total'][0]['count'] if agg_result and agg_result[0]['total'] else 0

        if self.pagination_class:
            paginator = self.pagination_class(request.args, total, request.endpoint)
            pipeline = pipeline + [{"$skip": paginator.skip}, {"$limit": paginator.limit}]
            results = list(self.model.aggregate(pipeline))
            meta = paginator.get_meta()
        else:
            results = list(self.model.aggregate(pipeline))
            meta = {}

        serializer = self.get_serializer()
        serialized_data = [serializer.to_representation(doc) for doc in results]
        return custom_response(data=serialized_data, total=total, **meta)

    @handle_api_errors
    def list(self):
        """GET / 获取列表（支持过滤、分页、聚合）"""
        filter_dict = self.get_filter_dict()
        pipeline = self.get_pipeline(filter_dict)
        if pipeline:
            return self._handle_aggregate_list(filter_dict, pipeline)
        return self._handle_normal_list(filter_dict)

    @handle_api_errors
    def create(self):
        """POST / 创建新资源"""
        data = request.json
        if not data:
            raise ValidationError("JSON body is required")
        serializer = self.get_serializer(data=data)
        if not serializer.is_valid(raise_exception=True):
            raise ValidationError(serializer.errors)
        validated_data = serializer.validated_data
        result = self.model.insert_one(validated_data)
        return custom_response(message="Created", code=201, id=str(result.inserted_id))

    @handle_api_errors
    def retrieve(self, id):
        """GET /<id> 获取单个资源"""
        if not ObjectId.is_valid(id):
            raise ValidationError("Invalid ID format")
        doc = self.model.find_one({"_id": ObjectId(id)})
        if not doc:
            raise NotFound("Resource not found")
        serializer = self.get_serializer(instance=doc)
        return custom_response(data=serializer.data())

    @handle_api_errors
    def update(self, id):
        """PUT /<id> 全量替换资源"""
        if not ObjectId.is_valid(id):
            raise ValidationError("Invalid ID format")
        data = request.json
        if not data:
            raise ValidationError("JSON body is required")
        # 检查原文档是否存在
        old_doc = self.model.find_one({"_id": ObjectId(id)})
        if not old_doc:
            raise NotFound("Resource not found")
        serializer = self.get_serializer(data=data)
        if not serializer.is_valid(raise_exception=True):
            raise ValidationError(serializer.errors)
        validated_data = serializer.validated_data
        validated_data['_id'] = old_doc['_id']  # 保留原 _id
        result = self.model.replace_by_id(id, validated_data)
        if result.matched_count == 0:
            raise NotFound("Resource not found")
        return custom_response(message="Updated", modified_count=result.modified_count)

    @handle_api_errors
    def partial_update(self, id):
        """PATCH /<id> 部分更新资源"""
        if not ObjectId.is_valid(id):
            raise ValidationError("Invalid ID format")
        data = request.json
        if not data:
            raise ValidationError("JSON body is required")
        old_doc = self.model.find_one({"_id": ObjectId(id)})
        if not old_doc:
            raise NotFound("Resource not found")
        serializer = self.get_serializer(instance=old_doc, data=data, partial=True)
        if not serializer.is_valid(raise_exception=True):
            raise ValidationError(serializer.errors)
        validated_data = serializer.validated_data
        result = self.model.update_one_by_id(id, validated_data)
        if result.matched_count == 0:
            raise NotFound("Resource not found")
        return custom_response(message="Partially Updated", modified_count=result.modified_count)

    @handle_api_errors
    def destroy(self, id):
        """DELETE /<id> 删除资源"""
        if not ObjectId.is_valid(id):
            raise ValidationError("Invalid ID format")
        result = self.model.delete_by_id(id)
        if result.deleted_count == 0:
            raise NotFound("Resource not found")
        return custom_response(message="Deleted", code=204)

    @classmethod
    def register_routes(cls, blueprint: Blueprint, url_prefix: str, actions: List[str] = None):
        """
        工业级路由注册，自动绑定 URL 规则和 Swagger 文档。
        """
        view_instance = cls()
        allowed = actions or ['list', 'create', 'retrieve', 'update', 'partial_update', 'destroy']
        all_specs = generate_swagger_config(cls)

        mapping = [
            ('', 'list', ['GET'], 'list'),
            ('', 'create', ['POST'], 'create'),
            ('/<id>', 'retrieve', ['GET'], 'retrieve'),
            ('/<id>', 'update', ['PUT'], 'update'),
            ('/<id>', 'partial_update', ['PATCH'], 'partial_update'),
            ('/<id>', 'destroy', ['DELETE'], 'destroy'),
        ]

        def make_view_func(method_name, method):
            @wraps(method)
            def view(*args, **kwargs):
                return method(*args, **kwargs)

            if method_name in all_specs:
                return swag_from(all_specs[method_name])(view)
            return view

        for suffix, method_name, http_methods, name_suffix in mapping:
            if method_name in allowed:
                current_method = getattr(view_instance, method_name)
                final_view = make_view_func(method_name, current_method)
                blueprint.add_url_rule(
                    f'/{url_prefix}{suffix}',
                    view_func=final_view,
                    methods=http_methods,
                    endpoint=f'{url_prefix}_{name_suffix}'
                )
