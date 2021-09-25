-- Notes:
--  The user used to create all this structure requires to have been granted the usual roles. Don't forget about the REFERENCES role, needed to create FOREIGN KEYs constraints.
--  All the VARCHAR columns use the special charset utf8mb4, which allows the storage of 1 to 4 bytes unicode symbols, unlike utf8, which allows only 1 to 3 bytes unicode symbols, leading to data corruption or security issues. See: https://mathiasbynens.be/notes/mysql-utf8mb4
--  As this is a personal project, I have decided not to take timezones in consideration in the DATETIME columns. Although, this must be dealt with in a more serious project. See: https://javorszky.co.uk/2016/06/06/today-i-learned-about-mysql-and-timezones/
--  The default collation is utf8mb4_bin, which allows the comparison of UTF-8 Unicode case sensitive strings. As utf8mb4_unicode_cs is not supported in my MySQL server, this one is used instead.

DROP DATABASE NewsAggregator;

-- NewsAggregator database
CREATE DATABASE NewsAggregator;

-- Use the database in order to create the following tables in it.
USE NewsAggregator;

-- Database tables.
-- users table
CREATE TABLE users (
    id INT AUTO_INCREMENT,
    name VARCHAR(25) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COLLATE utf8mb4_bin,
    surname VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin,
    email VARCHAR(25) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
    password VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
    is_active BOOLEAN DEFAULT TRUE NOT NULL,
    PRIMARY KEY(id),
    UNIQUE KEY(email)
) COMMENT = 'Signed up users in the application';

-- rss_feeds table
CREATE TABLE rss_feeds (
    id INT AUTO_INCREMENT,
    url VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
    title VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin,
    PRIMARY KEY(id),
    UNIQUE KEY(url)
) COMMENT = 'Sites that expose their news using RSS';

-- rss_feeds_news table
CREATE TABLE rss_feeds_news (
    id INT AUTO_INCREMENT,
    rss_feed_id INT NOT NULL,
    query_date DATETIME,
    news_data JSON,
    PRIMARY KEY(id),
    CONSTRAINT rss_feeds_news_rss_feeds_id_fk FOREIGN KEY(rss_feed_id) REFERENCES rss_feeds(id) ON DELETE CASCADE
) COMMENT = 'News obtained from the RSS sites stored in the "rss_feeds" table. Every row in this table will hold all the news received from a RSS feed in a given date. This information will be used as:
    1. Cache to avoid calls to news sites made by different users in a short period of time.
    2. Store a history of news for later use (maybe as a library of some kind).';

-- tags table
CREATE TABLE tags (
    id INT AUTO_INCREMENT,
    title VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
    description VARCHAR(400) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin,
    PRIMARY KEY(id)
) COMMENT = 'Tags will be used to classify the RSS feeds and identify users interests';

-- rss_feeds_tags table
CREATE TABLE rss_feeds_tags (
    rss_feed_id INT,
    tag_id INT,
    PRIMARY KEY(rss_feed_id, tag_id),
    CONSTRAINT rss_feeds_tags_rss_feeds_id_fk FOREIGN KEY(rss_feed_id) REFERENCES rss_feeds(id) ON DELETE CASCADE,
    CONSTRAINT rss_feeds_tags_tags_id_fk FOREIGN KEY(tag_id) REFERENCES tags(id) ON DELETE CASCADE
) COMMENT = 'Relationship between RSS sites and tags. Each RSS site may have more than one tag, giving information about the type of content they publish to potential subscribers';

-- subscriptions table
CREATE TABLE subscriptions (
    user_id INT,
    rss_feed_id INT,
    PRIMARY KEY(user_id, rss_feed_id),
    CONSTRAINT subscriptions_users_id_fk FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT subscriptions_rss_feeds_id_fk FOREIGN KEY(rss_feed_id) REFERENCES rss_feeds(id) ON DELETE CASCADE
) COMMENT = 'Users subscribed to RSS feeds';

'
-- sessions table
-- OAuth and Stateless APIs will not use classic sessions to operate.
CREATE TABLE sessions (
    id INT AUTO_INCREMENT,
    user_id INT NOT NULL,
    session_id VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
    creation_date DATETIME DEFAULT NOW() NOT NULL,
    expiration_date DATETIME NOT NULL,
    closing_date DATETIME,
    is_alive BOOLEAN DEFAULT TRUE NOT NULL,
    PRIMARY KEY(id),
    CONSTRAINT sessions_users_id_fk FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY(session_id),
    INDEX(user_id)
) COMMENT = \'All the sessions that users create when they log-in will be stored here\';
'