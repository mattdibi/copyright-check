import pytest

from copyright_check import check_header
from copyright_check import Error

import textwrap

def test_check_header():

    template = textwrap.dedent('''\
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
        ''')

    assert check_header('test/resources/test.java', template, "text/x-java", True) == None
