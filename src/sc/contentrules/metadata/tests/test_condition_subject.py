# -*- coding:utf-8 -*-
from plone.app.contentrules.rule import Rule
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.contentrules.engine.interfaces import IRuleStorage
from plone.contentrules.rule.interfaces import IExecutable
from plone.contentrules.rule.interfaces import IRuleCondition
from Products.CMFCore.PortalContent import PortalContent
from sc.contentrules.metadata.conditions.subject import SubjectCondition
from sc.contentrules.metadata.conditions.subject import SubjectEditForm
from sc.contentrules.metadata.testing import INTEGRATION_TESTING
from zope.component import getUtility, getMultiAdapter
from zope.component.interfaces import IObjectEvent
from zope.interface import implements

import unittest2 as unittest


class DummyEvent(object):
    implements(IObjectEvent)

    def __init__(self, object):
        self.object = object


class TestSubjectCondition(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'folder')
        self.folder = self.portal['folder']
        self.folder.setSubject(['Foo', ])
        sub_folder_id = self.folder.invokeFactory('Folder', 'sub_folder')
        self.sub_folder = self.folder[sub_folder_id]
        self.sub_folder.setSubject(['Bar', ])
        o = PortalContent('cmf', 'CMF Content', '', '', '')
        self.folder._setObject('cmf', o, suppress_events=True)

    def test_registered(self):
        element = getUtility(IRuleCondition,
                             name='sc.contentrules.conditions.Subject')
        self.assertEquals('sc.contentrules.conditions.Subject',
                          element.addview)
        self.assertEquals('edit', element.editview)
        self.assertEquals(None, element.for_)
        self.assertEquals(IObjectEvent, element.event)

    def test_invoke_add_view(self):
        element = getUtility(IRuleCondition,
                             name='sc.contentrules.conditions.Subject')
        storage = getUtility(IRuleStorage)
        storage[u'foo'] = Rule()
        rule = self.portal.restrictedTraverse('++rule++foo')

        adding = getMultiAdapter((rule, self.portal.REQUEST),
                                 name='+condition')
        addview = getMultiAdapter((adding, self.portal.REQUEST),
                                  name=element.addview)

        addview.createAndAdd(data={'subject': ['Foo', ]})

        e = rule.conditions[0]
        self.failUnless(isinstance(e, SubjectCondition))
        self.assertEquals(['Foo', ], e.subject)

    def test_invoke_edit_view(self):
        element = getUtility(IRuleCondition,
                             name='sc.contentrules.conditions.Subject')
        e = SubjectCondition()
        editview = getMultiAdapter((e, self.folder.REQUEST),
                                   name=element.editview)
        self.failUnless(isinstance(editview, SubjectEditForm))

    def test_execute(self):
        e = SubjectCondition()
        e.subject = ['Foo', ]

        ex = getMultiAdapter((self.portal, e, DummyEvent(self.folder)),
                             IExecutable)
        self.assertEquals(True, ex())

        ex = getMultiAdapter((self.portal, e, DummyEvent(self.sub_folder)),
                             IExecutable)
        self.assertEquals(False, ex())

        e.subject = ['Bar', ]
        ex = getMultiAdapter((self.portal, e, DummyEvent(self.sub_folder)),
                             IExecutable)
        self.assertEquals(True, ex())

    def test_execute_multivalued(self):
        e = SubjectCondition()
        e.subject = ['Foo', 'Bar', ]

        ex = getMultiAdapter((self.portal, e, DummyEvent(self.folder)),
                             IExecutable)
        self.assertEquals(True, ex())

        ex = getMultiAdapter((self.portal, e, DummyEvent(self.sub_folder)),
                             IExecutable)
        self.assertEquals(True, ex())

    def test_execute_empty(self):
        e = SubjectCondition()
        e.subject = []

        ex = getMultiAdapter((self.portal, e, DummyEvent(self.folder)),
                             IExecutable)
        self.assertEquals(False, ex())

        ex = getMultiAdapter((self.portal, e, DummyEvent(self.sub_folder)),
                             IExecutable)
        self.assertEquals(False, ex())

        # Empty Subject field
        self.sub_folder.setSubject([])
        ex = getMultiAdapter((self.portal, e, DummyEvent(self.sub_folder)),
                             IExecutable)
        self.assertEquals(True, ex())

    def test_execute_object_without_subject(self):
        e = SubjectCondition()
        e.subject = ['Foo', 'Bar', ]

        ex = getMultiAdapter((self.folder, e,
                              DummyEvent(self.folder['cmf'])),
                             IExecutable)
        self.assertEquals(False, ex())
