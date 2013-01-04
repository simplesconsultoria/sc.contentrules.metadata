# -*- coding:utf-8 -*-
from plone.app.contentrules.rule import Rule
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.contentrules.engine.interfaces import IRuleStorage
from plone.contentrules.rule.interfaces import IExecutable
from plone.contentrules.rule.interfaces import IRuleAction
from sc.contentrules.metadata.actions.creators import CreatorsAction
from sc.contentrules.metadata.actions.creators import CreatorsEditForm
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


class TestCreatorsAction(unittest.TestCase):

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
        self.document.setCreators(('foo', ))
        self.document.reindexObject()

    def test_registered(self):
        element = getUtility(IRuleAction,
                             name='sc.contentrules.actions.Creators')
        self.assertEquals('sc.contentrules.actions.Creators',
                          element.addview)
        self.assertEquals('edit', element.editview)
        self.assertEquals(None, element.for_)
        self.assertEquals(IObjectEvent, element.event)

    def test_invoke_add_view(self):
        element = getUtility(IRuleAction,
                             name='sc.contentrules.actions.Creators')
        storage = getUtility(IRuleStorage)
        storage[u'foo'] = Rule()
        rule = self.portal.restrictedTraverse('++rule++foo')

        adding = getMultiAdapter((rule, self.portal.REQUEST),
                                 name='+action')
        addview = getMultiAdapter((adding, self.portal.REQUEST),
                                  name=element.addview)

        addview.createAndAdd(data={'creators': ('bar', ),
                                   'only_empty': False})

        e = rule.actions[0]
        self.failUnless(isinstance(e, CreatorsAction))
        self.assertEquals(('bar', ), e.creators)
        self.assertEquals(False, e.only_empty)

    def test_invoke_edit_view(self):
        element = getUtility(IRuleAction,
                             name='sc.contentrules.actions.Creators')
        e = CreatorsAction()
        editview = getMultiAdapter((e, self.folder.REQUEST),
                                   name=element.editview)
        self.failUnless(isinstance(editview, CreatorsEditForm))

    def test_execute(self):
        e = CreatorsAction()
        e.creators = ('bar', )
        e.only_empty = False

        ex = getMultiAdapter((self.folder, e,
                             DummyEvent(self.sub_folder)),
                             IExecutable)
        self.assertEquals(True, ex())

        self.assertEquals(self.sub_folder.Creators(),
                          e.creators)

    def test_execute_only_if_empty(self):
        e = CreatorsAction()
        e.creators = ('bar', )
        e.only_empty = True

        ex = getMultiAdapter((self.folder, e,
                             DummyEvent(self.document)),
                             IExecutable)
        self.assertEquals(False, ex())

        self.assertNotEquals(self.document.Creators(),
                             e.creators)

    def test_execute_empty(self):
        e = CreatorsAction()
        e.creators = ('bar', )
        e.only_empty = False

        ex = getMultiAdapter((self.folder, e,
                             DummyEvent(self.document)),
                             IExecutable)
        self.assertEquals(True, ex())

        self.assertEquals(self.document.Creators(),
                          e.creators)
