# responses.py
from typing import Any
from flask import jsonify
from bson import ObjectId
from datetime import datetime, date


def _serialize_deep(obj: Any) -> Any:
    """深度序列化，用于 custom_response 中的额外字段（非 results）"""
    if isinstance(obj, ObjectId):
        return str(obj)
    if isinstance(obj, (datetime, date)):
        return obj.strftime("%Y-%m-%d %H:%M:%S")
    if isinstance(obj, list):
        return [_serialize_deep(item) for item in obj]
    if isinstance(obj, dict):
        return {k: _serialize_deep(v) for k, v in obj.items()}
    return obj


def custom_response(data=None, total=0, message="success", code=200, **kwargs):
    response_body = {
        "code": code,
        "message": message,
        "data": data,  # data 应该已经是序列化好的（由 Serializer 处理）
        "total": total,
        "success": True if 200 <= code < 300 else False
    }
    if kwargs:
        # 对额外字段进行深度序列化
        response_body.update(_serialize_deep(kwargs))
    return jsonify(response_body), code
