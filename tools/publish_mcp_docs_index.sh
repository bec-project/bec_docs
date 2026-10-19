#!/usr/bin/env bash
set -euo pipefail

index_file=${1:?Usage: bash tools/publish_mcp_docs_index.sh INDEX_FILE}
: "${GITEA_REGISTRY_TOKEN:?Missing registry credentials (username:token)}"
if [[ ! -r "$index_file" || ! -s "$index_file" ]]; then
  echo "Index file must be readable and non-empty: $index_file" >&2
  exit 1
fi

package_url="https://gitea.psi.ch/api/packages/bec/generic/bec_docs_index/latest"
task_response=$(mktemp)
trap 'rm -f "$task_response"' EXIT
task_auth=$(printf '%s' "$GITEA_REGISTRY_TOKEN" | base64 | tr -d '\n')
# Generic packages cannot overwrite a file; remove the previous latest version.
status=$(printf 'header = "Authorization: Basic %s"\n' "$task_auth" | \
  curl --config - --silent --show-error --output "$task_response" \
    --write-out '%{http_code}' --request DELETE "$package_url")
case "$status" in
  204|404) ;;
  *) echo "Registry deletion failed (HTTP $status)" >&2; exit 1 ;;
esac
printf 'header = "Authorization: Basic %s"\n' "$task_auth" | \
  curl --config - --fail-with-body --silent --show-error \
    --upload-file "$index_file" \
    "$package_url/bec_docs_index.json.gz"
