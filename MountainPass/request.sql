
-- -------------------------------------------------------------
-- Database, modified: pereval
-- Generation Time: 2022-05-10
-- -------------------------------------------------------------

-- This script only contains the table creation statements and does not fully represent the table in the database. It's still missing: indices, triggers.

-- Sequence and defined type
CREATE SEQUENCE IF NOT EXISTS user_id_seq;

-- Table Definition
CREATE TABLE "public"."users" (
    "id" int4 NOT NULL DEFAULT nextval('user_id_seq'::regclass),
    "email" varchar(50) NOT NULL UNIQUE,
    "fam" varchar(30) NOT NULL,
    "name" varchar(30) NOT NULL,
    "otc" varchar(30) NOT NULL,
    "phone" varchar(11) NOT NULL,
    PRIMARY KEY ("id")
);

--    CONSTRAINT "user_unique" UNIQUE ("email")

-- This script only contains the table creation statements and does not fully represent the table in the database. It's still missing: indices, triggers.

-- Sequence and defined type
CREATE SEQUENCE IF NOT EXISTS coords_id_seq;

-- Table Definition
CREATE TABLE "public"."coords" (
    "id" int4 NOT NULL DEFAULT nextval('coords_id_seq'::regclass),
    "latitude" float8 NOT NULL,
    "longitude" float8 NOT NULL,
    "height" int4 NOT NULL,
    PRIMARY KEY ("id")
);

-- This script only contains the table creation statements and does not fully represent the table in the database. It's still missing: indices, triggers.

-- Sequence and defined type
CREATE SEQUENCE IF NOT EXISTS pereval_id_seq;

-- Table Definition
CREATE TABLE "public"."pereval_added" (
    "id" int4 NOT NULL DEFAULT nextval('pereval_id_seq'::regclass),
    "add_time" timestamp DEFAULT now(),
    "date_added" timestamp,
    "user_id" int4 NOT NULL REFERENCES users,
    "coords_id" int4 REFERENCES coords ON DELETE CASCADE,
    "status" varchar(15) DEFAULT 'new' NOT NULL,
    "beauty_title" varchar(10) NOT NULL,
    "title" varchar(100) NOT NULL,
    "other_titles" varchar(500) NOT NULL,
    "connect" varchar(3) DEFAULT ', ' NOT NULL,
    "winter" varchar(2),
    "summer" varchar(2),
    "autumn" varchar(2),
    "spring" varchar(2),
    PRIMARY KEY ("id")
);

--    CONSTRAINT pereval_added_users_id_fk_user_ob FOREIGN KEY (user_id),
--    CONSTRAINT pereval_added_coords_id_fk_coords_ob FOREIGN KEY (coords_id)

-- This script only contains the table creation statements and does not fully represent the table in the database. It's still missing: indices, triggers. Do not use it as a backup.

-- Sequence and defined type
CREATE SEQUENCE IF NOT EXISTS pereval_areas_id_seq;

-- Table Definition
CREATE TABLE "public"."pereval_areas" (
    "id" int8 NOT NULL DEFAULT nextval('pereval_areas_id_seq'::regclass),
    "id_parent" int8 NOT NULL,
    "title" text,
    PRIMARY KEY ("id")
);

-- This script only contains the table creation statements and does not fully represent the table in the database. It's still missing: indices, triggers. Do not use it as a backup.

-- Sequence and defined type
CREATE SEQUENCE IF NOT EXISTS pereval_added_id_seq;

-- Table Definition
CREATE TABLE "public"."pereval_images" (
    "id" int4 NOT NULL DEFAULT nextval('pereval_added_id_seq'::regclass),
    "pereval_id" int4 REFERENCES "pereval_added" ON DELETE CASCADE,
    "date_added" timestamp DEFAULT now(),
    "name_file" varchar(50) NOT NULL UNIQUE,
    "img" bytea,
    PRIMARY KEY ("id")
);

-- This script only contains the table creation statements and does not fully represent the table in the database. It's still missing: indices, triggers. Do not use it as a backup.

-- Sequence and defined type
CREATE SEQUENCE IF NOT EXISTS untitled_table_200_id_seq;

-- Table Definition
CREATE TABLE "public"."spr_activities_types" (
    "id" int4 NOT NULL DEFAULT nextval('untitled_table_200_id_seq'::regclass),
    "title" text,
    PRIMARY KEY ("id")
);

-- Test data
INSERT INTO "public"."users" (
    "id",
    "email",
    "phone",
    "fam",
    "name",
    "otc"
) VALUES (
    1,
    'user@email.tld',
    '79031234567',
    'Пупкин',
    'Василий',
    'Иванович'
);


INSERT INTO "public"."coords" (
    "id",
    "latitude",
    "longitude",
    "height"
) VALUES (
    1,
    45.3842,
    7.1525,
    1200
);


INSERT INTO "public"."pereval_added" (
    "id",
    "user_id",
    "coords_id",
    "date_added",
    "beauty_title",
    "title",
    "other_titles",
    "connect",
    "add_time",
    "winter",
    "summer",
    "autumn",
    "spring"
) VALUES (1, 1, 1, '2022-02-21 14:14:00.720184', 'пер. ', 'Пхия', 'Триев', ', ', '2021-09-22 13:18:13.720184', '', '1А', '1А', '');


INSERT INTO "public"."pereval_areas" ("id", "id_parent", "title") VALUES
(0, 0, 'Планета Земля'),
(1, 0, 'Памиро-Алай'),
(65, 0, 'Алтай'),
(66, 65, 'Северо-Чуйский хребет'),
(88, 65, 'Южно-Чуйский хребет'),
(92, 65, 'Катунский хребет'),
(105, 1, 'Фанские горы'),
(106, 1, 'Гиссарский хребет (участок западнее перевала Анзоб)'),
(131, 1, 'Матчинский горный узел'),
(133, 1, 'Горный узел Такали, Туркестанский хребет'),
(137, 1, 'Высокий Алай'),
(147, 1, 'Кичик-Алай и Восточный Алай'),
(367, 375, 'Аладаглар'),
(375, 0, 'Тавр'),
(384, 0, 'Саяны'),
(386, 65, 'Хребет Листвяга'),
(387, 65, 'Ивановский хребет'),
(388, 65, 'Массив Мунгун-Тайга'),
(389, 65, 'Хребет Цаган-Шибэту'),
(390, 65, 'Хребет Чихачева (Сайлюгем)'),
(391, 65, 'Шапшальский хребет'),
(392, 65, 'Хребет Южный Алтай'),
(393, 65, 'Хребет Монгольский Алтай'),
(398, 384, 'Западный Саян'),
(399, 384, 'Восточный Саян'),
(402, 384, 'Кузнецкий Алатау'),
(459, 65, 'Курайский хребет');

INSERT INTO "public"."pereval_images" ("id", "pereval_id", "date_added", "name_file") VALUES
(1, 1, '2022-02-21 14:21:51.796151', 'Седловина'),
(2, 1, '2022-02-21 14:21:52.896351', 'Подъем');

INSERT INTO "public"."spr_activities_types" ("id", "title") VALUES
(1, 'пешком'),
(2, 'лыжи'),
(3, 'катамаран'),
(4, 'байдарка'),
(5, 'плот'),
(6, 'сплав'),
(7, 'велосипед'),
(8, 'автомобиль'),
(9, 'мотоцикл'),
(10, 'парус'),
(11, 'верхом');
