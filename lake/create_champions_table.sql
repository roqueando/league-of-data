create table if not exists minio.league_data.champions(
	version VARCHAR,
	id VARCHAR,
	key VARCHAR,
	name VARCHAR,
	info ROW(attack INTEGER, defense INTEGER, magic INTEGER, difficulty INTEGER),
	tags "VARCHAR",
	stats ROW(
		hp INTEGER,
		hpperlevel INTEGER,
		mp INTEGER,
		mpperlevel INTEGER,
		movespeed INTEGER,
		armor INTEGER,
		armorperlevel DOUBLE,
		spellblock INTEGER,
		spellblockperlevel DOUBLE,
		attackrange INTEGER,
		hpregen INTEGER,
		hpregenperlevel DOUBLE,
		mpregen INTEGER,
		mpregenperlevel DOUBLE,
		crit INTEGER,
		critperlevel INTEGER,
		attackdamage INTEGER,
		attackdamageperlevel INTEGER,
		attackspeedperlevel DOUBLE,
		attackspeed DOUBLE
	)

) with (format = 'JSON', external_location='s3a://league-data/champions/');
