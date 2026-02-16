DROP table IF EXISTS deploys_2;
CREATE TABLE deploys_2  (
  id TEXT not null PRIMARY KEY,
  transaction_hash TEXT not null,
  ledger_sequence bigint not null,
  created_at timestamp not null,
  contract_id text,
  contract_name text,
  deployer text,
  version text,
  wasm_name text
)
