# Data Product API

To run this web service [Python Poetry](https://python-poetry.org/docs/#installation) **must** be installed.

```bash
# Install virtual environment
poetry install

# Activate virtual environment
poetry activate

# Initialize SQLite database
flask --app data_product_api init-db

# Start web service
flask --app data_product_api run --debug
```
