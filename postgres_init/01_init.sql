CREATE SCHEMA IF NOT EXISTS content;

GRANT ALL PRIVILEGES ON SCHEMA content TO mesa_user;

ALTER ROLE mesa_user IN DATABASE mesa_db SET search_path TO content, public;