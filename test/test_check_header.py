import pytest

from copyright_check import check_header
from copyright_check import Error

import textwrap

def test_check_header_kura():
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
    ''').strip()

    assert check_header('test/resources/valid.java', template, "text/x-java", True) == None
    assert check_header('test/resources/comma_separated_year.java', template, "text/x-java", True) == None
    assert check_header('test/resources/dash_separated_year.java', template, "text/x-java", True) == Error.HEADER_INCORRECT
    assert check_header('test/resources/missing.java', template, "text/x-java", True) == Error.HEADER_MISSING
    assert check_header('test/resources/incorrect.java', template, "text/x-java", True) == Error.HEADER_INCORRECT
    assert check_header('test/resources/invalidyear.java', template, "text/x-java", False) == Error.YEAR_INCORRECT

def test_check_header_esf():
    template = textwrap.dedent('''\
        ******************************************************************************
         * Copyright (c) {years} Eurotech and/or its affiliates. All rights reserved.
         ******************************************************************************
    ''').strip()

    assert check_header('test/resources/validesf.java', template, "text/x-java", True) == None
    assert check_header('test/resources/valid.java', template, "text/x-java", True) == Error.HEADER_INCORRECT
    assert check_header('test/resources/validesf.java', template, "text/x-java", False) == Error.YEAR_INCORRECT
