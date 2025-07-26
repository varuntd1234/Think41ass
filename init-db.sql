-- Database initialization script
-- This script runs when the PostgreSQL container starts for the first time

-- Create the database if it doesn't exist
SELECT 'CREATE DATABASE conversational_ai'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'conversational_ai')\gexec

-- Connect to the database
\c conversational_ai;

-- Create extensions if needed
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- The actual tables will be created by SQLAlchemy when the backend starts
-- This script ensures the database exists and is ready for the application 