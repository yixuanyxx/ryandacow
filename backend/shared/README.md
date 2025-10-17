# Shared Components for PSA Workforce Compass Microservices

This directory contains shared components used across all microservices.

## Components

### Database Connection
- `database.py` - Supabase connection and configuration
- `models.py` - Shared data models
- `exceptions.py` - Custom exception classes

### Authentication
- `auth.py` - JWT token validation and user authentication
- `middleware.py` - Common middleware functions

### Utilities
- `validators.py` - Common validation functions
- `helpers.py` - Utility functions
- `constants.py` - Shared constants and enums

## Usage

Each microservice imports from this shared package:

```python
from shared.database import get_db_connection
from shared.auth import verify_token
from shared.models import User, Skill
```
