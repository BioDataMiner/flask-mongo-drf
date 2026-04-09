# 🚀 flask-mongo-drf

[![PyPI version](https://badge.fury.io/py/flask-mongo-drf.svg)](https://badge.fury.io/py/flask-mongo-drf)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Documentation Status](https://readthedocs.org/projects/flask-mongo-drf/badge/?version=latest)](https://flask-mongo-drf.readthedocs.io/en/latest/?badge=latest)

An industrial-grade Flask framework for building RESTful APIs with MongoDB, featuring **automatic Swagger documentation**, **dependency injection**, and **production-ready patterns**.

## 🌟 Key Features

- **Generic ViewSets**: Rapidly build CRUD APIs with minimal boilerplate code.
- **Dependency Injection**: Decoupled Model and Database layers for superior testability.
- **Auto-Generated Swagger**: Dynamically generate OpenAPI documentation from your code.
- **Multi-Database Support**: Seamlessly manage multiple MongoDB connections.
- **Advanced Filtering**: Built-in `FilterSet` with multiple lookup expressions (`icontains`, `exact`, `gt`, `lt`, etc.).
- **Flexible Pagination**: Customizable pagination with configurable page sizes.
- **Serialization & Validation**: Declarative field validation with `Serializer` classes.
- **Error Handling**: Unified exception handling and standardized JSON responses.

## 📦 Installation

Install from PyPI:

```bash
pip install flask-mongo-drf
```

Or install from source:

```bash
git clone https://github.com/BioDataMiner/flask-mongo-drf.git
cd flask-mongo-drf
pip install -e .
```

## 🚀 Quick Start

### 1. Define Your Model

```python
from flask_mongo_drf import MongoBaseModel
from flask_mongo_drf.contrib import MongoDBManager


class UserModel(MongoBaseModel):
    def __init__(self):
        collection = MongoDBManager.get_collection(
            collection_name="users",
            client_name="default"
        )
        super().__init__(collection=collection)
```

### 2. Create a Serializer

```python
from flask_mongo_drf import Serializer


class UserSerializer(Serializer):
    username = CharField(required=True, max_length=100)
    email = CharField(required=True)
    age = IntegerField(required=False)
```

### 3. Build a ViewSet

```python
from flask_mongo_drf import MongoModelViewSet


class UserViewSet(MongoModelViewSet):
    model_class = UserModel
    serializer_class = UserSerializer
    filterset_class = UserFilterSet
    pagination_class = MongoPagination
```

### 4. Register Routes

```python
from flask import Flask, Blueprint

app = Flask(__name__)
api_bp = Blueprint('api', __name__)

UserViewSet.register_routes(api_bp, url_prefix='users')
app.register_blueprint(api_bp, url_prefix='/api/v1')

if __name__ == '__main__':
    app.run(debug=True)
```

### 5. Access Swagger UI

Visit `http://localhost:5000/apidocs/` to explore your auto-generated API documentation.

## 📚 Documentation

Full documentation is available at [ReadTheDocs](https://flask-mongo-drf.readthedocs.io/).

### Core Modules

| Module | Purpose |
| :--- | :--- |
| `mongo_models.py` | Base model class with CRUD operations |
| `mongo_viewsets.py` | Generic ViewSet for rapid API development |
| `mongo_serializers.py` | Field validation and data serialization |
| `mongo_filters.py` | Query filtering with multiple lookup types |
| `mongo_paginations.py` | Flexible pagination implementation |
| `mongo_responses.py` | Standardized JSON response formatting |
| `mongo_swagger.py` | Auto-generated Swagger documentation |
| `mongo_decorators.py` | Error handling and middleware decorators |
| `mongo_exceptions.py` | Custom exception classes |
| `contrib/mongodb_manager.py` | Multi-database connection management |

## 🧪 Testing

Run the test suite:

```bash
pytest tests/ -v
```

Run with coverage:

```bash
pytest tests/ --cov=flask_mongo_drf --cov-report=html
```

## 📖 Example Project

A complete example project is available in the `examples/` directory:

```bash
cd examples/monitor
pip install -r requirements.txt
python manage.py
```

Then visit `http://localhost:5050/apidocs/` to see the example API.

## 🛠️ Architecture

### Dependency Injection Pattern

The framework uses **constructor-based dependency injection** to decouple the Model layer from database connection logic:

```
┌─────────────────────────────────────────┐
│         Flask Application               │
│  ┌─────────────────────────────────┐   │
│  │    MongoDBManager               │   │
│  │  (Connection Factory)           │   │
│  └──────────┬──────────────────────┘   │
│             │                           │
│             ▼                           │
│  ┌─────────────────────────────────┐   │
│  │    Collection Instance          │   │
│  │  (PyMongo)                      │   │
│  └──────────┬──────────────────────┘   │
│             │                           │
│             ▼                           │
│  ┌─────────────────────────────────┐   │
│  │    MongoBaseModel               │   │
│  │  (Business Logic)               │   │
│  └──────────┬──────────────────────┘   │
│             │                           │
│             ▼                           │
│  ┌─────────────────────────────────┐   │
│  │    MongoModelViewSet            │   │
│  │  (REST Endpoints)               │   │
│  └─────────────────────────────────┘   │
└─────────────────────────────────────────┘
```

## 🔧 Configuration

### Multi-Database Setup

```python
from flask_mongo_drf.contrib import MongoDBManager, init_mongodb

# Register multiple MongoDB clients
MongoDBManager.register_client(
    name="primary",
    uri="mongodb://user:pass@localhost:27017/db1",
    default_db="db1"
)

MongoDBManager.register_client(
    name="secondary",
    uri="mongodb://user:pass@localhost:27017/db2",
    default_db="db2"
)

# Initialize with Flask app
init_mongodb(app)
```

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/amazing-feature`).
3. Commit your changes (`git commit -m 'Add amazing feature'`).
4. Push to the branch (`git push origin feature/amazing-feature`).
5. Open a Pull Request.

Please ensure all tests pass and add new tests for your changes.

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by Django REST Framework's clean API design.
- Built on top of Flask and PyMongo.
- Thanks to the open-source community for feedback and contributions.

## 📞 Support

For issues, questions, or suggestions, please open an issue on [GitHub](https://github.com/BioDataMiner/flask-mongo-drf/issues).

---

**Made with ❤️ by the flask-mongo-drf**
