# USPTO ODP API

Base URL: `https://api.uspto.gov`

Authentication header: `X-API-KEY: <key from USPTO_ODP_API_KEY>`

Primary endpoints used by the bundled server:

- `GET /api/v1/patent/applications/search`
- `GET /api/v1/patent/applications/{applicationNumber}`
- `GET /api/v1/patent/applications/{applicationNumber}/meta-data`
- `GET /api/v1/patent/applications/{applicationNumber}/continuity`
- `GET /api/v1/patent/applications/{applicationNumber}/transactions`
- `GET /api/v1/patent/applications/{applicationNumber}/documents`
- `GET /api/v1/patent/applications/{applicationNumber}/assignment`
- `GET /api/v1/patent/applications/{applicationNumber}/foreign-priority`

Search uses ODP query syntax, for example:

```text
applicationMetaData.inventionTitle:(nutrition OR calorie) AND applicationMetaData.applicationTypeLabelName:Utility
```

```text
applicationMetaData.patentNumber:10049598
```

```text
inventors.inventorNameText:"Smith"
```

Start with broad synonyms and then narrow. Keep `limit` modest, log the retrieval date, and preserve the complete query string in research workpapers.

The API and portal evolve. Confirm endpoint and field behavior against the current ODP documentation before large or automated runs. Handle HTTP 401/403 as credential or account-state issues and HTTP 429 as rate limiting.
