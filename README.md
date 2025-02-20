# copyright-check
Copyright checker

> [!WARNING]
> Development moved to [https://github.com/eclipse-kura/copyright-check](https://github.com/eclipse-kura/copyright-check)

## Requirements

- [libmagic](https://pypi.org/project/python-magic/)

## Usage

```bash
usage: copyright-check [-h] [-d] -c CONFIG file [file ...]

Check copyright headers

positional arguments:
  file                 file(s) to check

options:
  -h, --help           show this help message and exit
  -d, --debug          Print debug information
  -c, --config CONFIG  set path to the config yaml file

Example usage: copyright-check -c config.yaml $(git diff --name-only) **/*.java
```

## Example configuration

```yaml
# Enable or disable the copyright date check
bypass_year_check: false
# In the template the user can specify two variables: {years} and {holder}
# - {years} will match the copyright years (regex: `\d{4}(,\s\d{4})?`)
# - {holder} will match the copyright holder (regex: `[\w\s\.]+`)
template_java: |
  ******************************************************************************
   * Copyright (c) {years} {holder} and/or its affiliates and others
   *
   * This program and the accompanying materials are made
   * available under the terms of the Eclipse Public License 2.0
   * which is available at https://www.eclipse.org/legal/epl-2.0/
   *
   * SPDX-License-Identifier: EPL-2.0
   *
   * Contributors:
   *  {holder}
template_xml: |2
      Copyright (c) {years} {holder} and/or its affiliates and others

      This program and the accompanying materials are made
      available under the terms of the Eclipse Public License 2.0
      which is available at https://www.eclipse.org/legal/epl-2.0/

      SPDX-License-Identifier: EPL-2.0

      Contributors:
       {holder}
# Ignore specific files and paths. The syntax and semantics are the same as in the .gitignore file.
ignore:
  - ignore.java
```

## Running tests

From the root of the project run:

```bash
uv run pytest
```
