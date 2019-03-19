DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS feedback;
DROP TABLE IF EXISTS comment;
DROP TABLE IF EXISTS tag;
DROP TABLE IF EXISTS post_tag_relation;

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
	like INTEGER DEFAULT 0,
	unlike INTEGER DEFAULT 0,
	PRIMARY KEY (post_id, author_id),
	FOREIGN KEY (post_id) REFERENCES post (id),
	FOREIGN KEY (author_id) REFERENCES user (id)
);

CREATE TABLE comment (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	content TEXT NOT NULL,
	author_id INTEGER NOT NULL,
	post_id INTEGER NOT NULL,
	created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	FOREIGN KEY (author_id) REFERENCES user (id)
	FOREIGN KEY (post_id) REFERENCES post (id)
);

CREATE TABLE tag (
	name TEXT NOT NULL PRIMARY KEY
);

CREATE TABLE post_tag_relation (
	post_id INTEGER NOT NULL,
	tag_name TEXT NOT NULL,
	PRIMARY KEY (post_id, tag_name),
	FOREIGN KEY (post_id) REFERENCES post (id),
	FOREIGN KEY (tag_name) REFERENCES tag (name)
);

INSERT INTO tag (name)
VALUES
	('technology'), ('history'), ('art'), ('science'), ('math'), ('life'), ('other');
