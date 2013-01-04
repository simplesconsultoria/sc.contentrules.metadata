# -*- coding:utf-8 -*-
from plone.app.contentrules.rule import Rule
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.contentrules.engine.interfaces import IRuleStorage
from plone.contentrules.rule.interfaces import IExecutable
from plone.contentrules.rule.interfaces import IRuleAction
from Products.CMFCore.PortalContent import PortalContent
from Products.CMFCore.PortalFolder import PortalFolder
from sc.contentrules.metadata.actions.subject import SubjectAction
from sc.contentrules.metadata.actions.subject import SubjectEditForm
from sc.contentrules.metadata.testing import INTEGRATION_TESTING
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.component.interfaces import IObjectEvent
from zope.interface import implements

import unittest2 as unittest


class DummyEvent(object):
    implements(IObjectEvent)

    def __init__(self, object):
        self.object = object


class TestSubjectAction(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'folder')
        self.folder = self.portal['folder']
        self.folder.setSubject(['Foo', ])
        self.folder.reindexObject()
        sub_folder_id = self.folder.invokeFactory('Folder', 'sub_folder')
        self.sub_folder = self.folder[sub_folder_id]
        self.document = self.folder[self.folder.invokeFactory('Document',
                                                              'a_document')]
        self.document.setSubject(['Bar', ])
        self.document.reindexObject()

        o = PortalContent('cmf', 'CMF Content', '', '', '')
        self.folder._setObject('cmf', o, suppress_events=True)
        o = PortalFolder('cmf_folder', 'CMF Folder', '')
        self.folder._setObject('cmf_folder', o, suppress_events=True)
        o = PortalContent('cmf', 'CMF Content', '', '', '')
        self.folder['cmf_folder']._setObject('cmf', o, suppress_events=True)

    def test_registered(self):
        element = getUtility(IRuleAction,
                             name='sc.contentrules.actions.Subject')
        self.assertEquals('sc.contentrules.actions.Subject',
                          element.addview)
        self.assertEquals('edit', element.editview)
        self.assertEquals(None, element.for_)
        self.assertEquals(IObjectEvent, element.event)

    def test_invoke_add_view(self):
        element = getUtility(IRuleAction,
                             name='sc.contentrules.actions.Subject')
        storage = getUtility(IRuleStorage)
        storage[u'foo'] = Rule()
        rule = self.portal.restrictedTraverse('++rule++foo')

        adding = getMultiAdapter((rule, self.portal.REQUEST),
                                 name='+action')
        addview = getMultiAdapter((adding, self.portal.REQUEST),
                                  name=element.addview)

        addview.createAndAdd(data={'same_as_parent': False,
                                   'subject': ['Foo', ]})

        e = rule.actions[0]
        self.failUnless(isinstance(e, SubjectAction))
        self.assertEquals(False, e.same_as_parent)
        self.assertEquals(['Foo', ], e.subject)

    def test_invoke_edit_view(self):
        element = getUtility(IRuleAction,
                             name='sc.contentrules.actions.Subject')
        e = SubjectAction()
        editview = getMultiAdapter((e, self.folder.REQUEST),
                                   name=element.editview)
        self.failUnless(isinstance(editview, SubjectEditForm))

    def test_execute_with_subject(self):
        e = SubjectAction()
        e.same_as_parent = False
        e.subject = ['Bar', ]

        ex = getMultiAdapter((self.folder, e,
                             DummyEvent(self.sub_folder)),
                             IExecutable)
        self.assertEquals(True, ex())

        self.assertEquals(list(self.sub_folder.Subject()),
                          e.subject)

    def test_execute_same_as_parent(self):
        e = SubjectAction()
        e.same_as_parent = True
        e.subject = []

        ex = getMultiAdapter((self.folder, e,
                             DummyEvent(self.sub_folder)),
                             IExecutable)
        self.assertEquals(True, ex())

        self.assertEquals(self.sub_folder.Subject(), self.folder.Subject())

    def test_execute_object_without_subject(self):
        e = SubjectAction()
        e.same_as_parent = False
        e.subject = ['Bar', ]
        o = self.folder['cmf']
        ex = getMultiAdapter((self.folder, e,
                             DummyEvent(o)),
                             IExecutable)
        self.assertEquals(False, ex())

    def test_execute_parent_without_subject(self):
        e = SubjectAction()
        e.same_as_parent = True
        e.subject = []
        folder = self.folder['cmf_folder']
        o = folder['cmf']
        ex = getMultiAdapter((folder, e,
                             DummyEvent(o)),
                             IExecutable)
        self.assertEquals(False, ex())
