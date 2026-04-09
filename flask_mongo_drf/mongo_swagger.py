# swagger.py
from typing import Type, Dict, Any


def generate_swagger_config(view_cls: Type) -> Dict[str, Any]:
    model_name = "Resource"
    if hasattr(view_cls, 'model_class') and view_cls.model_class:
        model_name = view_cls.model_class.__name__.replace("Model", "")

    query_parameters = []
    if hasattr(view_cls, 'filterset_class') and view_cls.filterset_class:
        for name, filter_obj in view_cls.filterset_class._declared_filters.items():
            swagger_type = "string"
            filter_class_name = filter_obj.__class__.__name__
            if "Number" in filter_class_name:
                swagger_type = "number"
            elif "Boolean" in filter_class_name:
                swagger_type = "boolean"
            query_parameters.append({
                "name": name,
                "in": "query",
                "type": swagger_type,
                "description": filter_obj.help_text or f"Filter by {name}",
                "required": False
            })

    path_id_param = {
        "name": "id",
        "in": "path",
        "type": "string",
        "required": True,
        "description": "Resource ObjectId"
    }

    specs = {
        "list": {
            "tags": [model_name],
            "summary": f"List {model_name}",
            "parameters": query_parameters + [
                {"name": "page", "in": "query", "type": "integer", "default": 1},
                {"name": "page_size", "in": "query", "type": "integer", "default": 10},
            ],
            "responses": {200: {"description": "Success"}}
        },
        "create": {
            "tags": [model_name],
            "summary": f"Create {model_name}",
            "parameters": [{"name": "body", "in": "body", "required": True, "schema": {"type": "object"}}],
            "responses": {201: {"description": "Created"}}
        },
        "retrieve": {
            "tags": [model_name],
            "summary": f"Retrieve {model_name}",
            "parameters": [path_id_param],
            "responses": {200: {"description": "Success"}}
        },
        "update": {
            "tags": [model_name],
            "summary": f"Full update {model_name}",
            "parameters": [path_id_param, {"name": "body", "in": "body", "required": True, "schema": {"type": "object"}}],
            "responses": {200: {"description": "Updated"}}
        },
        "partial_update": {
            "tags": [model_name],
            "summary": f"Partial update {model_name}",
            "parameters": [path_id_param, {"name": "body", "in": "body", "required": True, "schema": {"type": "object"}}],
            "responses": {200: {"description": "Partially updated"}}
        },
        "destroy": {
            "tags": [model_name],
            "summary": f"Delete {model_name}",
            "parameters": [path_id_param],
            "responses": {204: {"description": "Deleted"}}
        }
    }
    return specs