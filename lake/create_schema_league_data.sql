-- Make sure that bucket `league-data` exists
CREATE SCHEMA IF NOT EXISTS minio.league_data WITH (location = 's3a://league-data/');
