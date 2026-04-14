#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HOME_DIR="${HOME}"
HERMES_HOME="${HERMES_HOME:-${HOME_DIR}/.hermes}"
PLUGIN_NAME="fleetmanager"
PLUGIN_SRC="${REPO_ROOT}/fleetmanager"
PLUGINS_DIR_ONE="${REPO_ROOT}/plugins"
PLUGINS_DIR_TWO="${HERMES_HOME}/plugins"
GITHUB_TARGET="${HOME_DIR}/.github"
ENV_FILE="${HERMES_HOME}/.env"
CONFIG_FILE="${HERMES_HOME}/config.yaml"
DEFAULT_PROVIDER="openrouter"
DEFAULT_OPENROUTER_MODEL="nvidia/nemotron-3-super-120b-a12b:free"

DB_NAME="${HERMES_FLEETMANAGER_DB:-hermes_fleetmanager}"
DB_USER="${HERMES_FLEETMANAGER_USER:-hermes_fleetmanager}"
DB_PASSWORD="${HERMES_FLEETMANAGER_PASSWORD:-hermes_fleetmanager}"
DB_HOST="${POSTGRES_HOST:-127.0.0.1}"
DB_PORT="${POSTGRES_PORT:-5432}"

log() {
  printf '[install] %s\n' "$1"
}

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || {
    printf 'Missing required command: %s\n' "$1" >&2
    exit 1
  }
}

append_env() {
  local key="$1"
  local value="$2"
  mkdir -p "$(dirname "${ENV_FILE}")"
  touch "${ENV_FILE}"
  if grep -q "^${key}=" "${ENV_FILE}"; then
    sed -i "s#^${key}=.*#${key}=${value}#" "${ENV_FILE}"
  else
    printf '%s=%s\n' "${key}" "${value}" >> "${ENV_FILE}"
  fi
}

ensure_config_model_defaults() {
  mkdir -p "$(dirname "${CONFIG_FILE}")"
  python3 - "${CONFIG_FILE}" "${DEFAULT_PROVIDER}" "${DEFAULT_OPENROUTER_MODEL}" <<'PY'
from pathlib import Path
import re
import sys

config_path = Path(sys.argv[1])
provider = sys.argv[2]
model = sys.argv[3]

text = config_path.read_text(encoding="utf-8") if config_path.exists() else ""

def render_model_block(body: str) -> str:
    lines = body.splitlines()
    updated = []
    found_provider = False
    found_default = False

    for line in lines:
        stripped = line.strip()
        if re.match(r"^provider:\s*", stripped):
            updated.append(f'  provider: "{provider}"')
            found_provider = True
            continue
        if re.match(r"^(default|model):\s*", stripped):
            updated.append(f'  default: "{model}"')
            found_default = True
            continue
        updated.append(line)

    if not found_provider:
        updated.append(f'  provider: "{provider}"')
    if not found_default:
        updated.append(f'  default: "{model}"')
    return "\n".join(updated).rstrip() + "\n"

match = re.search(r"(?ms)^model:\s*\n(?P<body>(?:^[ \t].*\n?)*)", text)
if match:
    body = match.group("body")
    replacement = "model:\n" + render_model_block(body)
    text = text[: match.start()] + replacement + text[match.end():]
else:
    if text and not text.endswith("\n"):
        text += "\n"
    text += (
        "model:\n"
        f'  provider: "{provider}"\n'
        f'  default: "{model}"\n'
    )

config_path.write_text(text, encoding="utf-8")
PY
}

install_postgres_if_needed() {
  if command -v psql >/dev/null 2>&1; then
    log 'PostgreSQL client already installed.'
    return
  fi
  if command -v apt-get >/dev/null 2>&1; then
    log 'Installing PostgreSQL server via apt-get.'
    sudo apt-get update
    sudo apt-get install -y postgresql postgresql-contrib
  else
    log 'Could not auto-install PostgreSQL; install it manually and rerun.'
    exit 1
  fi
}

ensure_db_and_user() {
  sudo systemctl enable --now postgresql >/dev/null 2>&1 || true
  sudo -u postgres psql -tAc "SELECT 1 FROM pg_roles WHERE rolname='${DB_USER}'" | grep -q 1 || \
    sudo -u postgres psql -c "CREATE USER ${DB_USER} WITH PASSWORD '${DB_PASSWORD}';"
  sudo -u postgres psql -tAc "SELECT 1 FROM pg_database WHERE datname='${DB_NAME}'" | grep -q 1 || \
    sudo -u postgres psql -c "CREATE DATABASE ${DB_NAME} OWNER ${DB_USER};"
}

main() {
  require_cmd python3

  mkdir -p "${PLUGINS_DIR_ONE}" "${PLUGINS_DIR_TWO}" "${GITHUB_TARGET}"

  log 'Symlinking plugin into local plugins directory.'
  ln -sfn "${PLUGIN_SRC}" "${PLUGINS_DIR_ONE}/${PLUGIN_NAME}"

  log 'Symlinking plugin into ~/.hermes/plugins.'
  ln -sfn "${PLUGIN_SRC}" "${PLUGINS_DIR_TWO}/${PLUGIN_NAME}"

  log 'Copying plugin .github assets into ~/.github.'
  cp -R "${REPO_ROOT}/.github/." "${GITHUB_TARGET}/"

  log 'Installing Python dependencies.'
  python3 -m pip install -r "${REPO_ROOT}/requirements.txt"

  install_postgres_if_needed
  ensure_db_and_user

  log 'Updating Hermes environment file.'
  append_env "POSTGRES_HOST" "${DB_HOST}"
  append_env "POSTGRES_PORT" "${DB_PORT}"
  append_env "POSTGRES_DB" "${DB_NAME}"
  append_env "POSTGRES_USER" "${DB_USER}"
  append_env "POSTGRES_PASSWORD" "${DB_PASSWORD}"
  append_env "DATABASE_URL" "postgresql://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}"

  log 'Setting Hermes default provider/model.'
  ensure_config_model_defaults

  log 'Installation complete.'
  log "Run full test suite with: cd ${REPO_ROOT} && ./tests.sh"
  log "Run pytest only with: pytest -o 'addopts=' ${REPO_ROOT}/tests -q"
}

main "$@"