# BEFORE DEPLOYING, BE SURE YOU CREATE NEW CREDENTIALS AND CONFIGS TO ENSURE SECURITY

# Credentials to connect to the local postgres database
# BE CAREFUL OF INCLUDING SPECIAL CHARS IN DB CREDENTIALS, MAY CAUSE BREAK WHEN RUNNING db_creation.py
LOCAL_DB_USER = "postgres"
LOCAL_DB_PASS = "localpost17"
LOCAL_DB_NAME = "trees"
LOCAL_DB_PORT = "5432" # should be 5432 or 5433

# Default credentials to store in the user table as the default admin user
ADMIN_USERNAME = "admin"
ADMIN_EMAIL = ""
ADMIN_NAME = "admin"
ADMIN_PASSWORD = "temp"

# Configurations for the backend user authentication system
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7" # to get a string like this run: openssl rand -hex 32
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 24

# Configuration for the database backup service
BACKUP_INTERVAL_DAYS = 30
