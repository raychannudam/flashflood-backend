PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY,
  username TEXT UNIQUE,
  email TEXT UNIQUE,
  status BOOLEAN DEFAULT 1,
  password TEXT,
  created_by INTEGER,
  updated_by INTEGER,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  FOREIGN KEY (created_by) REFERENCES users (id),
  FOREIGN KEY (updated_by) REFERENCES users (id)
);

CREATE TABLE IF NOT EXISTS telegram_accounts (
  id INTEGER PRIMARY KEY,
  user_id INTEGER,
  username TEXT UNIQUE,
  status BOOLEAN DEFAULT 1,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users (id)
);

CREATE TABLE IF NOT EXISTS phone_numbers (
  id INTEGER PRIMARY KEY,
  user_id INTEGER,
  phone_number TEXT UNIQUE,
  status BOOLEAN DEFAULT 1,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users (id)
);

CREATE TABLE IF NOT EXISTS alert_services (
  id INTEGER PRIMARY KEY,
  name TEXT,
  status BOOLEAN DEFAULT 1,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS users_alert_services (
  id INTEGER PRIMARY KEY,
  alert_service_id INTEGER,
  user_id INTEGER,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  FOREIGN KEY (alert_service_id) REFERENCES alert_services (id),
  FOREIGN KEY (user_id) REFERENCES users (id)
);

CREATE TABLE IF NOT EXISTS users_alert_services_users (
  users_alert_services_user_id INTEGER,
  users_id INTEGER,
  PRIMARY KEY (users_alert_services_user_id, users_id),
  FOREIGN KEY (users_alert_services_user_id) REFERENCES users_alert_services (id),
  FOREIGN KEY (users_id) REFERENCES users (id)
);

CREATE TABLE IF NOT EXISTS users_alert_services_alert_services (
  users_alert_services_alert_service_id INTEGER,
  alert_services_id INTEGER,
  PRIMARY KEY (users_alert_services_alert_service_id, alert_services_id),
  FOREIGN KEY (users_alert_services_alert_service_id) REFERENCES users_alert_services (id),
  FOREIGN KEY (alert_services_id) REFERENCES alert_services (id)
);
