#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PARENT_DIR="$(dirname "${ROOT_DIR}")"
LINE_LENGTH=120
DRY_RUN=false

resolve_cmd() {
  local name="$1"
  local candidate
  for candidate in \
    "${ROOT_DIR}/.venv/bin/${name}" \
    "${PARENT_DIR}/.venv/bin/${name}"; do
    if [[ -x "${candidate}" ]]; then
      printf '%s\n' "${candidate}"
      return 0
    fi
  done
  command -v "${name}"
}

require_cmd() {
  local name="$1"
  if ! resolve_cmd "${name}" >/dev/null 2>&1; then
    printf 'Missing required command: %s\n' "${name}" >&2
    exit 1
  fi
}

run_cmd() {
  if [[ "${DRY_RUN}" == true ]]; then
    printf '+'
    for arg in "$@"; do
      printf ' %q' "${arg}"
    done
    printf '\n'
    return 0
  fi
  echo "$@"
  "$@"
}

main() {
  if [[ "${1:-}" == "--dry-run" ]]; then
    DRY_RUN=true
  fi

  cd "${ROOT_DIR}"

  require_cmd ruff
  require_cmd mypy
  require_cmd autopep8
  require_cmd black
  require_cmd flake8
  require_cmd python3

  local ruff_bin mypy_bin autopep8_bin black_bin flake8_bin python_bin
  ruff_bin="$(resolve_cmd ruff)"
  mypy_bin="$(resolve_cmd mypy)"
  autopep8_bin="$(resolve_cmd autopep8)"
  black_bin="$(resolve_cmd black)"
  flake8_bin="$(resolve_cmd flake8)"
  python_bin="$(resolve_cmd python3)"
  pyright_bin="$(resolve_cmd pyright || true)"

  run_cmd "${ruff_bin}" check . --fix --config "line-length=${LINE_LENGTH}"  
  run_cmd "${autopep8_bin}" --in-place --recursive --max-line-length "${LINE_LENGTH}" .
  run_cmd "${black_bin}" --line-length "${LINE_LENGTH}" .
  run_cmd "${flake8_bin}" --max-line-length="${LINE_LENGTH}" --extend-ignore=E203 .
  run_cmd "${mypy_bin}" --ignore-missing-imports --check-untyped-defs .
  if [[ -n "${pyright_bin}" ]]; then
    run_cmd "${pyright_bin}" --project pyrightconfig.json || true
  else
    printf 'pyright not found in PATH; skipping Pyright/Pylance check\n'
  fi
  run_cmd "${python_bin}" -m pytest -o addopts= tests -q
}

main "$@"