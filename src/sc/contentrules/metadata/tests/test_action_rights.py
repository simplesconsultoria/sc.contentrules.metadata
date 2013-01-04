# -*- coding:utf-8 -*-
from plone.app.contentrules.rule import Rule
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.contentrules.engine.interfaces import IRuleStorage
from plone.contentrules.rule.interfaces import IExecutable
from plone.contentrules.rule.interfaces import IRuleAction
from sc.contentrules.metadata.actions.rights import RightsAction
from sc.contentrules.metadata.actions.rights import RightsEditForm
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


class TestRightsAction(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'folder')
        self.folder = self.portal['folder']
        sub_folder_id = self.folder.invokeFactory('Folder', 'sub_folder')
        self.sub_folder = self.folder[sub_folder_id]
        self.document = self.folder[self.folder.invokeFactory('Document',
                                                              'a_document')]
        self.document.setRights('Copyright Foo Bar')
        self.document.reindexObject()

    def test_registered(self):
        element = getUtility(IRuleAction,
                             name='sc.contentrules.actions.Rights')
        self.assertEquals('sc.contentrules.actions.Rights',
                          element.addview)
        self.assertEquals('edit', element.editview)
        self.assertEquals(None, element.for_)
        self.assertEquals(IObjectEvent, element.event)

    def test_invoke_add_view(self):
        element = getUtility(IRuleAction,
                             name='sc.contentrules.actions.Rights')
        storage = getUtility(IRuleStorage)
        storage[u'foo'] = Rule()
        rule = self.portal.restrictedTraverse('++rule++foo')

        adding = getMultiAdapter((rule, self.portal.REQUEST),
                                 name='+action')
        addview = getMultiAdapter((adding, self.portal.REQUEST),
                                  name=element.addview)

        addview.createAndAdd(data={'rights': 'Creative Commons 2.0',
                                   'only_empty': False})

        e = rule.actions[0]
        self.failUnless(isinstance(e, RightsAction))
        self.assertEquals('Creative Commons 2.0', e.rights)
        self.assertEquals(False, e.only_empty)

    def test_invoke_edit_view(self):
        element = getUtility(IRuleAction,
                             name='sc.contentrules.actions.Rights')
        e = RightsAction()
        editview = getMultiAdapter((e, self.folder.REQUEST),
                                   name=element.editview)
        self.failUnless(isinstance(editview, RightsEditForm))

    def test_execute(self):
        e = RightsAction()
        e.rights = 'Creative Commons 2.0'
        e.only_empty = False

        ex = getMultiAdapter((self.folder, e,
                             DummyEvent(self.sub_folder)),
                             IExecutable)
        self.assertEquals(True, ex())

        self.assertEquals(self.sub_folder.Rights(),
                          e.rights)

    def test_execute_only_if_empty(self):
        e = RightsAction()
        e.rights = 'Creative Commons 2.0'
        e.only_empty = True

        ex = getMultiAdapter((self.folder, e,
                             DummyEvent(self.document)),
                             IExecutable)
        self.assertEquals(False, ex())

        self.assertNotEquals(self.document.Rights(),
                             e.rights)

    def test_execute_empty(self):
        e = RightsAction()
        e.rights = 'Creative Commons 2.0'
        e.only_empty = False

        ex = getMultiAdapter((self.folder, e,
                             DummyEvent(self.document)),
                             IExecutable)
        self.assertEquals(True, ex())

        self.assertEquals(self.document.Rights(),
                          e.rights)
