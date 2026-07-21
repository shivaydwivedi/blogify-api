"""OpenAPI schema generation settings."""

SPECTACULAR_SETTINGS = {
    "TITLE": "Blogify API",
    "DESCRIPTION": "REST API for a modern blogging platform.",
    "VERSION": "0.1.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "COMPONENT_SPLIT_REQUEST": True,
    "SECURITY": [{"BearerAuth": []}],
    "COMPONENTS": {
        "securitySchemes": {
            "BearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
            },
        },
    },
}
