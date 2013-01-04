# -*- coding: utf-8 -*-
from doctest import DocFileSuite
from doctest import REPORT_ONLY_FIRST_FAILURE
from plone.testing import layered
from sc.contentrules.metadata.testing import FUNCTIONAL_TESTING

import unittest2 as unittest

optionflags = REPORT_ONLY_FIRST_FAILURE


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(DocFileSuite('functional/cpanel_action_contributors.txt',
                             optionflags=optionflags),
                layer=FUNCTIONAL_TESTING),
        layered(DocFileSuite('functional/cpanel_action_creators.txt',
                             optionflags=optionflags),
                layer=FUNCTIONAL_TESTING),
        layered(DocFileSuite('functional/cpanel_action_exclude_from_nav.txt',
                             optionflags=optionflags),
                layer=FUNCTIONAL_TESTING),
        layered(DocFileSuite('functional/cpanel_action_language.txt',
                             optionflags=optionflags),
                layer=FUNCTIONAL_TESTING),
        layered(DocFileSuite('functional/cpanel_action_rights.txt',
                             optionflags=optionflags),
                layer=FUNCTIONAL_TESTING),
        layered(DocFileSuite('functional/cpanel_action_subject.txt',
                             optionflags=optionflags),
                layer=FUNCTIONAL_TESTING),
        layered(DocFileSuite('functional/cpanel_condition_subject.txt',
                             optionflags=optionflags),
                layer=FUNCTIONAL_TESTING),
    ])
    return suite
