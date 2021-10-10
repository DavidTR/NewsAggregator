-- Notes:
--  The user used to create all this structure requires to have been granted the usual roles. Don't forget about the REFERENCES role, needed to create FOREIGN KEYs constraints.
--  All the VARCHAR columns use the special charset utf8mb4, which allows the storage of 1 to 4 bytes unicode symbols, unlike utf8, which allows only 1 to 3 bytes unicode symbols, leading to data corruption or security issues. See: https://mathiasbynens.be/notes/mysql-utf8mb4
--  As this is a personal project, I have decided not to take timezones in consideration in the DATETIME columns. Although, this must be dealt with in a more serious project. See: https://javorszky.co.uk/2016/06/06/today-i-learned-about-mysql-and-timezones/
--  The default collation is utf8mb4_bin, which allows the comparison of UTF-8 Unicode case sensitive strings. As utf8mb4_unicode_cs is not supported in my MySQL server, this one is used instead.

DROP DATABASE NewsAggregatorBackend;

-- NewsAggregator database
CREATE DATABASE NewsAggregatorBackend;

-- Use the database in order to create the following tables in it.
USE NewsAggregatorBackend;

-- Database tables.
-- users table
CREATE TABLE users (
    id INT AUTO_INCREMENT,
    name VARCHAR(25) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin,
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
    title VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin,
    url VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
    last_update_date DATETIME,
    PRIMARY KEY(id),
    UNIQUE KEY(url)
) COMMENT = 'Sites that expose their news using RSS';

-- rss_feeds_news table
CREATE TABLE rss_feeds_news (
    id INT AUTO_INCREMENT,
    rss_feed_id INT NOT NULL,
    query_date DATETIME,
    news_data MEDIUMTEXT,
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
    subscription_date DATETIME DEFAULT NOW(),
    PRIMARY KEY(user_id, rss_feed_id),
    CONSTRAINT subscriptions_users_id_fk FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT subscriptions_rss_feeds_id_fk FOREIGN KEY(rss_feed_id) REFERENCES rss_feeds(id) ON DELETE CASCADE
) COMMENT = 'Users subscribed to RSS feeds';


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
) COMMENT = 'All the sessions that users create when they log-in will be stored here';


-- Test data (comment if not needed)
-- Both passwords are the same: PaSsw?!-;ord
INSERT INTO users(name, surname, email, password) VALUES ('Test 1', 'Test test', 'test1@test.com', '$2b$12$zrsEukigKo7kgiLiEjHx4OB1I9qHfcedAcQsYZb2qmEPcSWOCfIRy'), ('Test 2', 'Test test', 'test2@test.com', '$2b$12$zrsEukigKo7kgiLiEjHx4OB1I9qHfcedAcQsYZb2qmEPcSWOCfIRy');
INSERT INTO rss_feeds(title, url) VALUES ('The Guardian', 'https://www.theguardian.com/world/rss'), ('Science news', 'https://www.sciencenews.org/feed');

-- Deleting the "\n" characters is mandatory to insert these records
INSERT INTO rss_feeds_news(rss_feed_id, query_date, news_data) VALUES (1, NOW(), '<item><title>Taliban publicly display bodies of alleged kidnappers in Herat</title><link>https://www.theguardian.com/world/2021/sep/25/taliban-publicly-display-bodies-of-alleged-kidnappers-in-herat</link><description><p>Four corpses taken to main square and hung from cranes by Afghanistan’s Islamist regime</p><p>Taliban authorities in the western Afghan city of Herat killed four alleged kidnappers and hung their bodies up in public to deter others, a local government official has said.</p><p>Sher Ahmad Ammar, the deputy governor of Herat, said on Saturday that the men had kidnapped a local businessman and his son and intended to take them out of the city, when they were seen by patrols that had set up checkpoints around the city.</p> <a href="https://www.theguardian.com/world/2021/sep/25/taliban-publicly-display-bodies-of-alleged-kidnappers-in-herat">Continue reading...</a></description><category domain="https://www.theguardian.com/world/afghanistan">Afghanistan</category><category domain="https://www.theguardian.com/law/human-rights">Human rights</category><category domain="https://www.theguardian.com/world/world">World news</category><pubDate>Sat, 25 Sep 2021 15:10:23 GMT</pubDate><guid>https://www.theguardian.com/world/2021/sep/25/taliban-publicly-display-bodies-of-alleged-kidnappers-in-herat</guid><media:content width="140" url="https://i.guim.co.uk/img/media/3c973d653aba1d6dc1edf05f892e9b1cf6a6d037/0_200_6000_3600/master/6000.jpg?width=140&quality=85&auto=format&fit=max&s=bfa7ab46495feb26dc3d68409f9206af"><media:credit scheme="urn:ebu">Photograph: AP</media:credit></media:content><media:content width="460" url="https://i.guim.co.uk/img/media/3c973d653aba1d6dc1edf05f892e9b1cf6a6d037/0_200_6000_3600/master/6000.jpg?width=460&quality=85&auto=format&fit=max&s=220f5df29dbf772db1fb8e8a4c133e2a"><media:credit scheme="urn:ebu">Photograph: AP</media:credit></media:content><dc:creator>Reuters</dc:creator><dc:date>2021-09-25T15:10:23Z</dc:date></item>'), (2, NOW(), '<item><title>Bloodthirsty vampire bats like to drink with friends over strangers</title><link>https://www.sciencenews.org/article/vampire-bats-drink-blood-friends-strangers-social</link><dc:creator><![CDATA[Jonathan Lambert]]></dc:creator><pubDate>Thu, 23 Sep 2021 18:00:00 +0000</pubDate><category><![CDATA[Animals]]></category><guid isPermaLink="false">https://www.sciencenews.org/?p=3104015</guid><description><![CDATA[Cooperation among vampire bats extends beyond the roost. New research suggests that bonded bats often drink blood from animals together. ]]></description><content:encoded><![CDATA[<p>Vampire bats may be bloodthirsty, but that doesn’t mean they can’t share a drink with friends.</p><p>Fights can erupt among bats over gushing wounds bit into unsuspecting animals. But bats that have bonded while roosting <a href="http://dx.doi.org/10.1371/journal.pbio.3001366">often team up to drink blood</a> away from home, researchers report September 23 in <em>PLOS Biology</em>.&nbsp;</p><p>Vampire bats (<em>Desmodus rotundus</em>) can <a href="https://www.sciencenews.org/article/vampire-bat-friendships-endure-captivity-wild">form long-term social bonds</a> with each other through grooming, sharing regurgitated blood meals and generally hanging out together at the roost (<em>SN: 10/31/19</em>). But whether these friendships, which occur between both kin and nonkin, extend to the bats’ nightly hunting had been unclear. “They’re flying around out there, but we didn’t know if they were still interacting with each other,” says Gerald Carter, an evolutionary biologist at Ohio State University in Columbus.</p><p>To find out, Carter and his colleague Simon Ripperger of the Museum für Naturkunde in Berlin, built on <a href="https://www.cell.com/current-biology/fulltext/S0960-9822(19)31364-8">previous research</a> that uncovered a colony’s social network using bat backpacks. Tiny computer sensors glued to 50 female bats in Tolé, Panama, continuously registered proximity to other sensors both within the roost and outside, revealing when bats met up while foraging.&nbsp;</p><figure class="wp-block-embed is-type-video is-provider-youtube wp-block-embed-youtube wp-embed-aspect-16-9 wp-has-aspect-ratio"><div class="wp-block-embed__wrapper"><iframe loading="lazy" title="Watch two vampire bats suck blood from a cow | Science News" width="500" height="281" src="https://www.youtube.com/embed/UMK_T24fptc?feature=oembed" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div><figcaption>Two common vampire bats feed on a cow near La Chorrera, Panama. It can take 10 to 40 minutes for a bat to bite a small, diamond-shaped wound into an animal’s flesh, and fights can sometimes break out over access to wounds. But researchers found that bats who are friendly back at the roost likely feed together in the field, potentially saving time and energy.</figcaption></figure><p>Bat buds rarely left the roost together, suggesting that they don’t go on tightly coordinated hunts, Carter says. But bats with a history of associating with one another were more likely than strangers to meet up in the field and likely feed together, the researchers found. Rendezvous with friends also lasted longer, on average, than other interactions. That was especially true for bats with many roost buddies.</p><p>“These are more or less haphazard encounters,” Carter says. He suspects that the bats mostly forage alone, but when they encounter a friendly bat on a cow, for instance, they’ll feed together instead of fighting or flying off to find other food. Biting a new wound can take 10 to 40 minutes, Carter says, so sharing with a friend could save these bloodthirsty bats time and energy.</p>]]></content:encoded><media:thumbnail url="https://www.sciencenews.org/wp-content/uploads/2021/09/092121_JL_vampire-bat-friends_feat_REV-330x186.jpg"></media:thumbnail><enclosureurl="https://www.sciencenews.org/wp-content/uploads/2021/09/092121_JL_vampire-bat-friends_feat_REV-330x186.jpg"length="231544"type="image/jpeg"></enclosure></item>');

INSERT INTO tags(title, description) VALUES ('Economy', 'World-wide economic news'), ('Science', 'Latest articles from all disciplines of science'), ('Politics', 'Why would you want to know about this?');
INSERT INTO rss_feeds_tags(rss_feed_id, tag_id) VALUES (1, 1), (1, 2), (2, 2);
INSERT INTO subscriptions(user_id, rss_feed_id) VALUES (1, 1), (1, 2), (2, 2);
