-- admin_keys definition

CREATE TABLE admin_keys (
	id TEXT,
	user_id INTEGER,
	creation_date TEXT,
	activation_date TEXT
);

-- configuration definition

CREATE TABLE configuration (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT,
	value TEXT
);

-- likes definition

CREATE TABLE likes (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	user_id_give INTEGER,
	user_id_get INTEGER,
	reason TEXT,
	creation_date TEXT,
	"type" TEXT);

-- promises definition

CREATE TABLE promises (
	id TEXT,
	request_text TEXT,
	promise_text TEXT,
	promise_date TEXT,
	promise_status TEXT,
	user_id_give INTEGER,
	user_id_get INTEGER,
	creation_date TEXT,
	remindes_count INTEGER
);

-- scheduled definition

CREATE TABLE scheduled (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	promise_id INTEGER,
	scheduled_datetime TEXT,
	status TEXT
);

-- settings definition

CREATE TABLE settings (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT,
	value TEXT,
	group_id INTEGER
);

-- superusers definition

CREATE TABLE superusers (
	id INTEGER
);

-- users definition

CREATE TABLE users (
	id INTEGER PRIMARY KEY,
	group_id INTEGER
);

-- users_stat definition

CREATE TABLE users_stat (
	id INTEGER PRIMARY KEY,
	likes INTEGER DEFAULT 0,
	dislikes INTEGER DEFAULT 0,
	trust REAL DEFAULT 0,
	username TEXT,
	state TEXT DEFAULT MAIN_MENU,
	selected_user INTEGER,
	selected_promise TEXT,
	FOREIGN KEY (id) REFERENCES users (id)
);