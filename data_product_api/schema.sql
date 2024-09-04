DROP TABLE IF EXISTS contracts;

CREATE TABLE contracts (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  consumer_data_product_name TEXT NOT NULL,
  consumer_data_product_contact TEXT NOT NULL,
  data_asset_name TEXT NOT NULL
);
