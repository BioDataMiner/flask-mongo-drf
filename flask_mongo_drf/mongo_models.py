# mongo_models.py
from bson import ObjectId
from datetime import datetime
from pymongo.collection import Collection
from typing import Dict, Any, List, Optional, Iterator
from pymongo.results import InsertOneResult, UpdateResult, DeleteResult


class MongoBaseModel:
    """
    MongoDB 基础模型类。
    通过依赖注入方式传入 PyMongo Collection 对象，与框架解耦。
    """

    def __init__(self, collection: Collection):
        """
        :param collection: PyMongo Collection 实例
        """
        self.collection = collection

    def count_documents(self, query: Dict[str, Any]) -> int:
        """统计文档数量"""
        return self.collection.count_documents(query)

    def find_all(self, query: Dict[str, Any], sort_by: str = None, sort_order: int = -1) -> Iterator[Dict[str, Any]]:
        """
        返回游标，避免一次性加载所有文档。
        若需要排序，传入 sort_by 字段名和 sort_order（1 升序，-1 降序）。
        """
        cursor = self.collection.find(query)
        if sort_by:
            cursor = cursor.sort(sort_by, sort_order)
        return cursor

    def find_paginated(
            self,
            query: Dict[str, Any],
            skip: int,
            limit: int,
            sort_by: str = "_id",
            sort_order: int = -1
    ) -> List[Dict[str, Any]]:
        """分页查询，返回文档列表"""
        cursor = self.collection.find(query).sort(sort_by, sort_order).skip(skip).limit(limit)
        return list(cursor)

    def insert_one(self, data: Dict[str, Any]) -> InsertOneResult:
        """插入单条文档，自动添加 create_time 和 update_time"""
        data.setdefault("create_time", datetime.now())
        data["update_time"] = datetime.now()
        return self.collection.insert_one(data)

    def update_one_by_id(self, doc_id: str, data: Dict[str, Any]) -> UpdateResult:
        """根据 _id 部分更新文档（PATCH）"""
        mongo_id = ObjectId(doc_id) if isinstance(doc_id, str) else doc_id
        data['update_time'] = datetime.now()
        return self.collection.update_one({"_id": mongo_id}, {"$set": data})

    def replace_by_id(self, doc_id: str, new_doc: Dict[str, Any]) -> UpdateResult:
        """根据 _id 全量替换文档（PUT）"""
        mongo_id = ObjectId(doc_id) if isinstance(doc_id, str) else doc_id
        new_doc['update_time'] = datetime.now()
        new_doc['_id'] = mongo_id
        return self.collection.replace_one({"_id": mongo_id}, new_doc)

    def delete_by_id(self, doc_id: str) -> DeleteResult:
        """根据 _id 删除文档"""
        mongo_id = ObjectId(doc_id) if isinstance(doc_id, str) else doc_id
        return self.collection.delete_one({"_id": mongo_id})

    def find_one(self, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """查询单条文档"""
        return self.collection.find_one(query)

    def aggregate(self, pipeline: List[Dict[str, Any]]):
        """执行聚合管道，返回游标"""
        return self.collection.aggregate(pipeline)
