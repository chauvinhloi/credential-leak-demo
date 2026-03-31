# Unity Catalog Query Runbook Using Client ID and Client Secret

This is a simple demo runbook for querying a Unity Catalog table with `curl`.

## 1. Set environment variables

```bash
export DATABRICKS_HOST="https://<your-workspace-host>"
export DATABRICKS_CLIENT_ID="<client-id>"
export DATABRICKS_CLIENT_SECRET="<client-secret>"
```

## 2. Get an OAuth access token

```bash
curl -s --request POST \
  "${DATABRICKS_HOST}/oidc/v1/token" \
  --user "${DATABRICKS_CLIENT_ID}:${DATABRICKS_CLIENT_SECRET}" \
  --data 'grant_type=client_credentials&scope=all-apis'
```

Copy the `access_token` from the response, then set it:

```bash
export DATABRICKS_TOKEN="<access-token>"
```

## 3. List SQL warehouses

Use this to discover the warehouse ID:

```bash
curl -s --request GET \
  "${DATABRICKS_HOST}/api/2.0/sql/warehouses" \
  --header "Authorization: Bearer ${DATABRICKS_TOKEN}"
```

## 4. Set the warehouse ID

```bash
export DATABRICKS_SQL_WAREHOUSE_ID="<warehouse-id>"
```

## 5. Run a query against a Unity Catalog table

```bash
curl -s --request POST \
  "${DATABRICKS_HOST}/api/2.0/sql/statements/" \
  --header "Authorization: Bearer ${DATABRICKS_TOKEN}" \
  --header "Content-Type: application/json" \
  --data '{
    "warehouse_id": "'"${DATABRICKS_SQL_WAREHOUSE_ID}"'",
    "statement": "SELECT * FROM XXX.XXX.XXX LIMIT 5"
  }' | jq
```

## 6. Poll the statement if needed

If the first response is `PENDING` or `RUNNING`, copy the `statement_id` from the response and set it:

```bash
export SQL_STATEMENT_ID="<statement-id>"
```

Then poll for the result:

```bash
curl -s --request GET \
  "${DATABRICKS_HOST}/api/2.0/sql/statements/${SQL_STATEMENT_ID}" \
  --header "Authorization: Bearer ${DATABRICKS_TOKEN}"
```

## Summary

1. Get OAuth token
2. List SQL warehouses
3. Set warehouse ID
4. Run query
5. Poll statement result if needed
