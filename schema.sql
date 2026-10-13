CREATE TABLE IF NOT EXISTS "backlog_books" (
    "id" INTEGER PRIMARY KEY,
    "title" TEXT NOT NULL,
    "l2_locale" TEXT,           -- works can be multilingual (war and peace). consider this further
    "created_at" TEXT,          -- for testing, i don't even know if it's gonna be useful
    "modified_at" TEXT          --  //   //
);

--  TODO: books ought to hold chapters/lessons, which hold records,
--  TODO: but records should be easily moved between chapters according to user discretion,
CREATE TABLE IF NOT EXISTS "extractions" (
    "id" INTEGER PRIMARY KEY,
    "position" INTEGER,         -- second most important record
    "l2_text" TEXT,             -- the most important record
--    "l2_locale" TEXT,           -- could live in the book instead; 99.9% of works out there are monolingual
    "created_at" TEXT,          -- for testing
    "modified_at" TEXT,         --  //   //
    "book_id" INTEGER REFERENCES "backlog_books"(id)
);

CREATE TABLE IF NOT EXISTS "translations" (
    "id" INTEGER PRIMARY KEY,
    "l1_locale" TEXT,
    "l1_text" TEXT,
    "created_at" TEXT,          -- for testing
    "modified_at" TEXT,         --  //   //
    "mt_provider" TEXT,         --  //   //
    "extraction_id" INTEGER REFERENCES "extractions"(id)
);

CREATE TABLE IF NOT EXISTS "voiceovers" (
    "id" INTEGER PRIMARY KEY,
    "audio_path" TEXT,
    "created_at" TEXT,          -- for testing
    "modified_at" TEXT,         --  //   //
    "tts_provider" TEXT,        --  //   //
    "voice_id" TEXT,            --  //   //
    "extraction_id" INTEGER REFERENCES "extractions"(id)
);