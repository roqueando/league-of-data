create table if not exists minio.league_data.versions(
	"n" ROW(
		"item" VARCHAR,
		"summoner" VARCHAR,
		"champion" VARCHAR,
		"language" VARCHAR
	)
) with (format = 'JSON', external_location='s3a://league-data/versions/');
