#!/usr/bin/env bash
set -euo pipefail

# scripts/run_remote_test.sh
# Usage examples:
#  ./scripts/run_remote_test.sh -k /path/to/key.pem -u ubuntu@1.2.3.4 -d /home/ubuntu/Trinity_Store_Backup/backend -n "api/tests.py::TestClass::test_method"
#  ./scripts/run_remote_test.sh --key /home/hadeed/Downloads/trinity_dev.pem --userhost user@host --node "api/tests.py::TestClass::test_method"

print_usage() {
  cat <<EOF
Usage: $0 [options]

Options:
  -k, --key       Path to your SSH private key (default: /home/hadeed/Downloads/trinity_dev.pem)
  -u, --userhost  SSH user and host (user@host)
  -d, --dir       Remote directory containing the repo (default: /home/hadeed/Trinity_Store_Backup/backend)
  -n, --node      Pytest node id to run (e.g. api/tests.py::TestClass::test_method). If omitted runs full file `api/tests.py`.
  -p, --port      SSH port (default: 22)
  -y, --yes       Don't prompt for confirmation (non-interactive)
  -o, --opts      Extra pytest options to append to the remote pytest command (quote if needed)
  -h, --help      Show this help and exit

Examples:
  # run a single node
  $0 -k /home/hadeed/Downloads/trinity_dev.pem -u ubuntu@1.2.3.4 -n "api/tests.py::TestClass::test_method"

  # run by substring
  $0 -k /home/hadeed/Downloads/trinity_dev.pem -u ubuntu@1.2.3.4 -n "-k partial_name" 

EOF
}

# defaults
KEY_DEFAULT="/home/hadeed/Downloads/trinity_dev.pem"
USERHOST=""
REMOTE_DIR="/home/hadeed/Trinity_Store_Backup/backend"
NODE=""
PORT=22

# parse args
while [[ $# -gt 0 ]]; do
  case "$1" in
    -k|--key) KEY="$2"; shift 2;;
    -u|--userhost) USERHOST="$2"; shift 2;;
    -d|--dir) REMOTE_DIR="$2"; shift 2;;
    -n|--node) NODE="$2"; shift 2;;
    -p|--port) PORT="$2"; shift 2;;
    -h|--help) print_usage; exit 0;;
    --) shift; break;;
    -*) echo "Unknown option: $1" >&2; print_usage; exit 1;;
    *) break;;
  esac
done

KEY=${KEY:-$KEY_DEFAULT}

if [[ -z "$USERHOST" ]]; then
  echo "Error: --userhost is required (e.g. ubuntu@1.2.3.4)" >&2
  print_usage
  exit 2
fi

# Build pytest command
if [[ -z "$NODE" ]]; then
  PYTEST_TARGET="api/tests.py"
else
  PYTEST_TARGET="$NODE"
fi

PYTEST_OPTS=${PYTEST_OPTS:-}

SSH_OPTS=( -i "${KEY}" -o IdentitiesOnly=yes -p "${PORT}" )

# show what we'll run
echo "SSH: ${USERHOST} (port ${PORT})"
echo "Remote dir: ${REMOTE_DIR}"
echo "Pytest target: ${PYTEST_TARGET}"
if [[ -n "$PYTEST_OPTS" ]]; then
  echo "Additional pytest options: ${PYTEST_OPTS}"
fi

echo
if [[ -z "${YES:-}" ]]; then
  read -p "Proceed? [y/N] " confirm || true
  confirm=${confirm:-N}
  if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
    echo "Aborted by user"
    exit 0
  fi
fi

# Run the remote command
ssh "${SSH_OPTS[@]}" ${USERHOST} \
  "cd \"${REMOTE_DIR}\" && pytest -q ${PYTEST_TARGET} ${PYTEST_OPTS}"
