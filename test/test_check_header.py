import pytest

from copyright_check import check_header
from copyright_check import Error

KURA_JAVA_TEMPLATE = '''\
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
'''.rstrip() # Remove trailing newline


ESF_JAVA_TEMPLATE = '''\
******************************************************************************
 * Copyright (c) {years} Eurotech and/or its affiliates. All rights reserved.
 ******************************************************************************
'''.rstrip()


KURA_XML_TEMPLATE = '''\
    Copyright (c) {years} {holder} and/or its affiliates and others

    This program and the accompanying materials are made
    available under the terms of the Eclipse Public License 2.0
    which is available at https://www.eclipse.org/legal/epl-2.0/

    SPDX-License-Identifier: EPL-2.0

    Contributors:
     {holder}
'''.rstrip()


@pytest.mark.parametrize(
    "template,filename,yearbypass,expected",
    [
        (KURA_JAVA_TEMPLATE, 'test/resources/valid.java', True, None),
        (KURA_JAVA_TEMPLATE, 'test/resources/comma_separated_year.java', True, None),
        (KURA_JAVA_TEMPLATE, 'test/resources/dash_separated_year.java', True, Error.HEADER_INCORRECT),
        (KURA_JAVA_TEMPLATE, 'test/resources/missing.java', True, Error.HEADER_MISSING),
        (KURA_JAVA_TEMPLATE, 'test/resources/incorrect.java', True, Error.HEADER_INCORRECT),
        (KURA_JAVA_TEMPLATE, 'test/resources/invalidyear.java', False, Error.YEAR_INCORRECT),

        (ESF_JAVA_TEMPLATE, 'test/resources/validesf.java', True, None),
        (ESF_JAVA_TEMPLATE, 'test/resources/invalidesf.java', True, Error.HEADER_INCORRECT),
        (ESF_JAVA_TEMPLATE, 'test/resources/invalidesf2.java', True, Error.HEADER_INCORRECT),
        (ESF_JAVA_TEMPLATE, 'test/resources/valid.java', True, Error.HEADER_INCORRECT),
        (ESF_JAVA_TEMPLATE, 'test/resources/validesf.java', False, Error.YEAR_INCORRECT),

        (KURA_XML_TEMPLATE, 'test/resources/valid.xml', True, None),
        (KURA_XML_TEMPLATE, 'test/resources/invalid.xml', True, Error.HEADER_INCORRECT),
        (KURA_XML_TEMPLATE, 'test/resources/valid.xml', False, Error.YEAR_INCORRECT),
    ])
def test_check_header(template, filename, yearbypass, expected):

    mime_type = "text/x-java" if filename.endswith(".java") else "text/xml"

    result = check_header(filename, template, mime_type, yearbypass)
    assert result.error == expected, f"Expected {expected}, but got {result.error} for \"{filename}\". Diff:\n{result.diff}"
