-- Stage 1 - Core proposal domain (v1)
-- Safe migration script (idempotent)

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS proposals (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  proposal_id TEXT NOT NULL UNIQUE,
  customer_name TEXT NOT NULL,
  title TEXT,
  status TEXT NOT NULL DEFAULT 'draft',
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_proposals_proposal_id ON proposals(proposal_id);
CREATE INDEX IF NOT EXISTS idx_proposals_status ON proposals(status);

CREATE TABLE IF NOT EXISTS proposal_items (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  proposal_id_ref INTEGER NOT NULL,
  item_code TEXT,
  item_description TEXT NOT NULL,
  quantity REAL NOT NULL DEFAULT 1,
  unit TEXT,
  unit_price REAL NOT NULL DEFAULT 0,
  total_price REAL NOT NULL DEFAULT 0,
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  FOREIGN KEY(proposal_id_ref) REFERENCES proposals(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_proposal_items_proposal_ref ON proposal_items(proposal_id_ref);

CREATE TABLE IF NOT EXISTS proposal_status_history (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  proposal_id_ref INTEGER NOT NULL,
  from_status TEXT,
  to_status TEXT NOT NULL,
  reason_code TEXT,
  actor TEXT,
  changed_at TEXT NOT NULL DEFAULT (datetime('now')),
  FOREIGN KEY(proposal_id_ref) REFERENCES proposals(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_status_history_proposal_ref ON proposal_status_history(proposal_id_ref);
CREATE INDEX IF NOT EXISTS idx_status_history_changed_at ON proposal_status_history(changed_at);

CREATE TABLE IF NOT EXISTS proposal_pricing (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  proposal_id_ref INTEGER NOT NULL,
  direct_cost_total REAL NOT NULL DEFAULT 0,
  overhead_pct REAL NOT NULL DEFAULT 0,
  tax_pct REAL NOT NULL DEFAULT 0,
  margin_pct REAL NOT NULL DEFAULT 0,
  final_price REAL NOT NULL DEFAULT 0,
  pricing_policy_version TEXT,
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  FOREIGN KEY(proposal_id_ref) REFERENCES proposals(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_proposal_pricing_proposal_ref ON proposal_pricing(proposal_id_ref);

CREATE TABLE IF NOT EXISTS proposal_files (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  proposal_id_ref INTEGER NOT NULL,
  file_kind TEXT NOT NULL,
  file_path TEXT NOT NULL,
  file_hash TEXT,
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  FOREIGN KEY(proposal_id_ref) REFERENCES proposals(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_proposal_files_proposal_ref ON proposal_files(proposal_id_ref);
CREATE INDEX IF NOT EXISTS idx_proposal_files_kind ON proposal_files(file_kind);
