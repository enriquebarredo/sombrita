CREATE TABLE IF NOT EXISTS "extractions" (
    "id" INTEGER PRIMARY KEY,
    "l2_text" TEXT,             -- the most important record
    "position" INTEGER,
    "l2_locale" TEXT,
    "timestamp" TEXT,           -- maybe time creation helps with organization?
    "book" TEXT,                -- TODO What source material are we studying?
);

CREATE TABLE IF NOT EXISTS "translations" (
    "id" INTEGER PRIMARY KEY,
    "l1_locale" TEXT,
    "l1_text" TEXT,
    "created_at" TEXT,          -- for testing
    "modified_at" TEXT,         --  //   //
    "mt_provider" TEXT,         --  //   //
    "extraction_id" INTEGER REFERENCES "extractions"(id),
);

CREATE TABLE IF NOT EXISTS "voiceovers" (
    "id" INTEGER PRIMARY KEY,
    "audio_path" TEXT,
    "created_at" TEXT,          -- for testing
    "modified_at" TEXT,         --  //   //
    "tts_provider" TEXT,        --  //   //
    "voice_id" TEXT,            --  //   //
    "extraction_id" INTEGER REFERENCES "extractions"(id),
);

CREATE TABLE IF NOT EXISTS "backlog_books" (
    "id" INTEGER PRIMARY KEY,
    "title" TEXT NOT NULL,
    "l2_locale" TEXT,   --


);