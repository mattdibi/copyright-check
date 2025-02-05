# copyright-check
Copyright checker

## Example configuration

```yaml
bypass_year_check: false
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

ignore:
  - ignore.java
```
