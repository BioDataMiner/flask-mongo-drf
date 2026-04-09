# 🚀 Monitor Example

This example demonstrates how to leverage the **`flask-mongo-drf`** framework to build a production-ready RESTful API for managing monitor paths. It showcases a complete CRUD implementation featuring dependency injection, dynamic filtering, and automated Swagger documentation.

---

## 🌟 Key Features Demonstrated

- **Decoupled Architecture**: Defining MongoDB models using `MongoBaseModel` with collection injection.
- **Robust Validation**: Creating serializers with built-in field validation.
- **Generic ViewSets**: Automatic generation of `list`, `create`, `retrieve`, `update`, and `destroy` endpoints.
- **Advanced Filtering**: Using `CharFilter` with `icontains` (case-insensitive substring) lookups.
- **Flexible Pagination**: Custom pagination with configurable page size limits.
- **Auto-Documentation**: Instant Swagger/OpenAPI UI integration.

---

## 📂 Project Structure

```text
examples/
├── config/
│   └── settings.py   # MongoDB connection configuration
├── monitor/
│   ├── __init__.py
│   ├── app.py        # Blueprint & Route registration
│   ├── models.py     # MongoDB Model (ScanMonitorPathModel)
│   ├── serializers.py# Data Validation (ScanMonitorPathSerializer)
│   ├── filters.py    # Query Filtering (ScanMonitorPathFilter)
│   ├── paginations.py# Custom Pagination (max_page_size=200)
│   ├── views.py      # ViewSet logic (ScanMonitorPathViewSet)
│   └── README.md     # You are here!
├── app.py            # Flask app factory & initialization
├── manage.py         # Entry point (Run the server)
└── requirements.txt  # Project dependencies
```

---

## 🛠️ Setup & Installation

### 1. Clone & Navigate
```bash
git clone https://github.com/BioDataMiner/flask-mongo-drf.git
cd flask-mongo-drf/examples/monitor
```

### 2. Install Dependencies
You can install the framework in editable mode (recommended for development):
```bash
pip install -e ../../
```
Or install requirements manually:
```bash
pip install flask pymongo flasgger flask-cors
```

### 3. Environment Configuration
Set the following variables to connect to your MongoDB instance:

| Variable | Description | Default |
| :--- | :--- | :--- |
| `MONGO_USER` | MongoDB username | *(Required)* |
| `MONGO_PASS` | MongoDB password | *(Required)* |
| `MONGO_HOST` | MongoDB host | `localhost` |
| `MONGO_PORT` | MongoDB port | `27017` |
| `BLOOD_DB_NAME` | Blood database name | `Blood` |
| `TUMOR_DB_NAME` | Tumor database name | `Tumor` |

**Quick Export (Linux/macOS):**
```bash
export MONGO_USER=admin MONGO_PASS=password123 MONGO_HOST=localhost
```

### Configuration Details

The framework supports **multi-database connections** through `config/settings.py`:

```python
class Config:
    MONGODB_SETTINGS = {
        "blood": {
            "host": get_mongo_uri(
                "MONGO_USER", "MONGO_PASS", "MONGO_HOST", "MONGO_PORT",
                db_env="BLOOD_DB_NAME", fallback_db="Blood",
                maxPoolSize=50
            ),
            "db": "Blood",
        },
        "tumor": {
            "host": get_mongo_uri(
                "MONGO_USER", "MONGO_PASS", "MONGO_HOST", "MONGO_PORT",
                db_env="TUMOR_DB_NAME", fallback_db="Tumor",
                maxPoolSize=100
            ),
            "db": "Tumor",
        },
    }
```

The `get_mongo_uri()` helper function:
- Automatically escapes credentials using `quote_plus()`.
- Supports fallback database names when environment variables are not set.
- Allows custom connection pool sizes and other MongoDB URI parameters.

### 4. Run the Server
```bash
python manage.py
```
The server will start at `http://0.0.0.0:5050`.

---

## 📖 API Reference

All endpoints are prefixed with `/api/v1/monitor-paths`.

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | List all paths (Supports filtering & pagination) |
| `POST` | `/` | Create a new monitor path |
| `GET` | `/<id>` | Retrieve a single path by ID |
| `PUT` | `/<id>` | Full update (Replace) |
| `DELETE`| `/<id>` | Delete a path |

### 🔍 Filtering
The list endpoint supports query parameters defined in `ScanMonitorPathFilter`:
- `monitor_path`: Case-insensitive substring match.
- `status`: Case-insensitive substring match.

**Example:**
`GET /api/v1/monitor-paths/?monitor_path=MGI-T7&status=active`

### 📑 Pagination
- `page`: Page number (default: `1`)
- `page_size`: Items per page (default: `10`, max: `200`)

---

## 📝 Request Schema

**POST / PUT Body:**
```json
{
  "monitor_path": "/data/runs/MGI-T7_001",
  "status": "active"
}
```
*Note: `create_time` and `update_time` are automatically managed by the framework.*

---

## 🎨 Swagger Documentation

Once the server is running, explore the interactive API docs at:

👉 **[http://localhost:5050/apidocs/](http://localhost:5050/apidocs/)**

---

## 🧪 Testing with cURL

**Create a record:**
```bash
curl -X POST "http://localhost:5050/api/v1/monitor-paths/" \
  -H "Content-Type: application/json" \
  -d '{"monitor_path": "/tmp/test", "status": "active"}'
```

**List with filters:**
```bash
curl -X GET "http://localhost:5050/api/v1/monitor-paths/?status=active&page_size=5"
```

---

## ⚠️ Troubleshooting

- **"Client 'tumor' not registered"**: Ensure `init_mongodb(app)` is called in `app.py` before any database access.
- **Connection Refused**: Verify your MongoDB service is active and the `MONGO_HOST`/`PORT` are correct.
- **Empty Results**: Check if your filter `lookup_expr` matches your data. Use `icontains` for partial matches or `exact` for strict equality.

---

---

## 📋 Core Application Files

### `config/settings.py`
Manages MongoDB connection settings with support for multiple databases:
- Dynamically constructs MongoDB URIs from environment variables.
- Handles credential escaping and connection pool configuration.
- Supports fallback database names for flexibility.

### `app.py`
Flask application factory that:
- Initializes the Flask app with CORS support.
- Calls `init_mongodb(app)` to register all MongoDB clients.
- Configures Swagger/Flasgger for auto-generated API documentation.
- Registers the `monitor` blueprint at `/api/v1`.
- Handles static file serving for SPA compatibility.

### `manage.py`
Entry point script that:
- Adds the project root to Python path for proper imports.
- Creates and runs the Flask app on `0.0.0.0:5050` with debug mode enabled.

---

## 🚀 Next Steps
1. **Multi-Database Models**: Create additional models for the `blood` database by following the same pattern as `ScanMonitorPathModel`.
2. **Validation**: Extend `serializers.py` with custom regex or range checks.
3. **Aggregations**: Override `get_pipeline` in `views.py` to use MongoDB's aggregation framework.
4. **Security**: Add Flask-JWT-Extended or custom decorators to `views.py` for authentication.
5. **Monitoring**: Integrate logging and metrics collection for production deployments.
