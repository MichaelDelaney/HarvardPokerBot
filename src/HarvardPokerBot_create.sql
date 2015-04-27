
-- tables
-- Table: actions
CREATE TABLE actions (
    id integer NOT NULL  PRIMARY KEY AUTOINCREMENT,
    "action" varchar(255) NOT NULL
);

-- Table: board_ranks
CREATE TABLE board_ranks (
    id integer NOT NULL  PRIMARY KEY AUTOINCREMENT,
    cards integer NOT NULL
);

-- Table: hand_ranks
CREATE TABLE hand_ranks (
    id integer NOT NULL  PRIMARY KEY AUTOINCREMENT,
    hands varchar(255) NOT NULL
);

-- Table: players
CREATE TABLE players (
    id integer NOT NULL  PRIMARY KEY,
    name varchar(255) NOT NULL
);

-- Table: rounds
CREATE TABLE rounds (
    id integer NOT NULL  PRIMARY KEY AUTOINCREMENT,
    round integer NOT NULL
);

-- Table: probabilities
CREATE TABLE probabilities (
    id integer NOT NULL  PRIMARY KEY,
    player integer NOT NULL,
    "action" integer NOT NULL,
    round integer NOT NULL,
    board_rank integer NOT NULL,
    hand_rank integer NOT NULL,
    probability decimal(25,25) NOT NULL DEFAULT 0,
    FOREIGN KEY (player) REFERENCES players (id),
    FOREIGN KEY ("action") REFERENCES actions (id),
    FOREIGN KEY (hand_rank) REFERENCES hand_ranks (id),
    FOREIGN KEY (board_rank) REFERENCES board_ranks (id),
    FOREIGN KEY (round) REFERENCES rounds (id)
);


-- populate

INSERT INTO actions (action) VALUES ("raised");
INSERT INTO actions (action) VALUES ("folded");
INSERT INTO actions (action) VALUES ("called");
INSERT INTO actions (action) VALUES ("bet");
INSERT INTO actions (action) VALUES ("checked");
INSERT INTO board_ranks (cards) VALUES ("3 of a kind");
INSERT INTO board_ranks (cards) VALUES ("3 cards in sequence");
INSERT INTO board_ranks (cards) VALUES ("3 suited cards");
INSERT INTO board_ranks (cards) VALUES ("a pair");
INSERT INTO board_ranks (cards) VALUES ("2 cards in sequence");
INSERT INTO board_ranks (cards) VALUES ("2 suited cards");
INSERT INTO board_ranks (cards) VALUES ("other");
INSERT INTO hand_ranks (hands) VALUES ("AA, KK, QQ, JJ, AKs");
INSERT INTO hand_ranks (hands) VALUES ("TT, AQs, AJs, KQs, AK");
INSERT INTO hand_ranks (hands) VALUES ("99, JTs, QJs, KJs, ATs, AQ");
INSERT INTO hand_ranks (hands) VALUES ("T9s, KQ, 88, QTs, 98s, J9s, AJ, KTs");
INSERT INTO hand_ranks (hands) VALUES ("77, 87s, Q9s, T8s, KJ, QJ, JT, 76s, 97s, Axs, 65s");
INSERT INTO hand_ranks (hands) VALUES ("66, AT, 55, 86s, KT, QT, 54s, K9s, J8s, 75s");
INSERT INTO hand_ranks (hands) VALUES ("44, J9, 64s, T9, 53s, 33, 98, 43s, 22, Kxs, T7s, Q8s");
INSERT INTO hand_ranks (hands) VALUES ("87, A9, Q9, 76, 42s, 32s, 96s, 85s, J8, J7s, 65, 54, 74s, K9, T8");
INSERT INTO hand_ranks (hands) VALUES ("other");
INSERT INTO rounds (round) VALUES ("pre_flop");
INSERT INTO rounds (round) VALUES ("flop");
INSERT INTO rounds (round) VALUES ("turn");
INSERT INTO rounds (round) VALUES ("river");


-- End of file.

