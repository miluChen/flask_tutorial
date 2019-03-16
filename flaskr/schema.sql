DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS feedback;

CREATE TABLE user (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	username TEXT UNIQUE NOT NULL,
	password TEXT NOT NULL
);

CREATE TABLE post (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	author_id INTEGER NOT NULL,
	created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	title TEXT NOT NULL,
	body TEXT NOT NULL,
	thumbsup INTEGER DEFAULT 0,
	thumbsdown INTEGER DEFAULT 0,
	FOREIGN KEY (author_id) REFERENCES user (id)
);

CREATE TABLE feedback (
	post_id INTEGER NOT NULL,
	author_id INTEGER NOT NULL,
	like BOOLEAN DEFAULT FALSE,
	unlike BOOLEAN DEFAULT FALSE,
	comment TEXT DEFAULT NULL,
	PRIMARY KEY (post_id, author_id),
	FOREIGN KEY (post_id) REFERENCES post (id),
	FOREIGN KEY (author_id) REFERENCES user (id)
);
