CREATE TABLE IF NOT EXISTS surgical_index (
  image_id TEXT PRIMARY KEY,
  s3_uri TEXT NOT NULL,
  anatomy TEXT NOT NULL,
  view_type TEXT NOT NULL,
  pelvic_tilt REAL NOT NULL,
  noise_sigma REAL NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

