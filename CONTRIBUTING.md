# Contributing

Contributions that improve correctness, safety, USPTO compatibility, documentation, or research quality are welcome.

1. Fork the repository and create a focused branch.
2. Do not add API keys, confidential invention material, private application records, or generated research reports.
3. Keep server operations read-only and dependency-free unless a change has a clear public benefit.
4. Add or update behavior tests for server changes.
5. Run:

   ```bash
   python3 -m unittest discover -s plugins/uspto-patent-research/tests -v
   python3 plugins/uspto-patent-research/server/uspto_mcp_server.py --self-test
   ```

6. Describe any live USPTO testing separately from offline tests and redact credentials and sensitive query material.

By contributing, you agree that your contribution is licensed under the MIT License.
