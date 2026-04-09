# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-04-08

### Added
- Initial release of flask-mongo-drf
- Generic `MongoModelViewSet` for rapid CRUD API development
- Dependency injection pattern for decoupled Model and Database layers
- Auto-generated Swagger/OpenAPI documentation via Flasgger
- Multi-database connection support with `MongoDBManager`
- Advanced filtering with `FilterSet` and multiple lookup expressions
- Flexible pagination with `MongoPagination`
- Declarative field validation with `Serializer` classes
- Unified exception handling with custom exception classes
- Comprehensive documentation and examples
- Full test coverage with pytest
- GitHub Actions CI/CD pipeline

### Features
- `MongoBaseModel`: Base class for MongoDB models with CRUD operations
- `MongoModelViewSet`: Generic ViewSet providing list, create, retrieve, update, partial_update, destroy
- `FilterSet`: Declarative filtering framework
- `Serializer`: Field validation and data serialization
- `MongoPagination`: Configurable pagination
- `MongoDBManager`: Multi-database connection factory
- Auto Swagger documentation generation

---

## [Unreleased]

### Planned
- GraphQL support
- Async/await support
- Rate limiting middleware
- JWT authentication integration
- Caching layer support
- Bulk operations
- Advanced aggregation pipeline builder

---

## Version History

### v1.0.0 (2026-04-08)
- 🎉 Initial stable release
