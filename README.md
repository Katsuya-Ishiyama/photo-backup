# photo-backup

## Settings in this repository

### How to set checking mechanism for code health

In this repository, checking listed below is recommended to retain code clean before commit.
This part introduces you how to set checking mechanism with "pre-commit".

1. Move current directory to the directory `.pre-commit-config.yaml` is put.
2. Activate git hooks of pre-commit.
   ```shell
   $ pre-commit install
   ```
