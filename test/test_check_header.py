import pytest

from copyright_check import check_header
from copyright_check import Error

import textwrap

@pytest.mark.parametrize(
    "filename,yearbypass,expected",
    [
        ('test/resources/valid.java',True, None),
        ('test/resources/comma_separated_year.java',True, None),
        ('test/resources/dash_separated_year.java',True, Error.HEADER_INCORRECT),
        ('test/resources/missing.java',True, Error.HEADER_MISSING),
        ('test/resources/incorrect.java',True, Error.HEADER_INCORRECT),
        ('test/resources/invalidyear.java',False, Error.YEAR_INCORRECT),
    ])
def test_check_header_kura_param(filename, yearbypass, expected):
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

    result = check_header(filename, template, "text/x-java", yearbypass)
    assert result.error == expected, f"Expected {expected}, but got {result.error}. Diff:\n{result.diff}"

@pytest.mark.parametrize(
    "filename,yearbypass,expected",
    [
        ('test/resources/validesf.java',True, None),
        ('test/resources/valid.java',True, Error.HEADER_INCORRECT),
        ('test/resources/validesf.java',False, Error.YEAR_INCORRECT),
    ])
def test_check_header_esf(filename, yearbypass, expected):
    template = textwrap.dedent('''\
        ******************************************************************************
         * Copyright (c) {years} Eurotech and/or its affiliates. All rights reserved.
         ******************************************************************************
    ''').strip()

    result = check_header(filename, template, "text/x-java", yearbypass)
    assert result.error == expected, f"Expected {expected}, but got {result.error}. Diff:\n{result.diff}"

@pytest.mark.parametrize(
    "filename,yearbypass,expected",
    [
        ('test/resources/valid.xml',True, None),
    ])
def test_check_header_kura_xml(filename, yearbypass, expected):
    template = '''\
    Copyright (c) {years} {holder} and/or its affiliates and others

    This program and the accompanying materials are made
    available under the terms of the Eclipse Public License 2.0
    which is available at https://www.eclipse.org/legal/epl-2.0/

    SPDX-License-Identifier: EPL-2.0

    Contributors:
    {holder}
    '''.strip()

    result = check_header(filename, template, "text/xml", yearbypass)
    assert result.error == expected, f"Expected {expected}, but got {result.error}. Diff:\n{result.diff}"
