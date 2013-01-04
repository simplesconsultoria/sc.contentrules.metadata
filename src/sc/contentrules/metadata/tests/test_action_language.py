# -*- coding:utf-8 -*-
from plone.app.contentrules.rule import Rule
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.contentrules.engine.interfaces import IRuleStorage
from plone.contentrules.rule.interfaces import IExecutable
from plone.contentrules.rule.interfaces import IRuleAction
from sc.contentrules.metadata.actions.language import LanguageAction
from sc.contentrules.metadata.actions.language import LanguageEditForm
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


class TestLanguageAction(unittest.TestCase):

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
        self.document.setLanguage('de')
        self.document.reindexObject()

    def test_registered(self):
        element = getUtility(IRuleAction,
                             name='sc.contentrules.actions.Language')
        self.assertEquals('sc.contentrules.actions.Language',
                          element.addview)
        self.assertEquals('edit', element.editview)
        self.assertEquals(None, element.for_)
        self.assertEquals(IObjectEvent, element.event)

    def test_invoke_add_view(self):
        element = getUtility(IRuleAction,
                             name='sc.contentrules.actions.Language')
        storage = getUtility(IRuleStorage)
        storage[u'foo'] = Rule()
        rule = self.portal.restrictedTraverse('++rule++foo')

        adding = getMultiAdapter((rule, self.portal.REQUEST),
                                 name='+action')
        addview = getMultiAdapter((adding, self.portal.REQUEST),
                                  name=element.addview)

        addview.createAndAdd(data={'language': 'en',
                                   'only_empty': False})

        e = rule.actions[0]
        self.failUnless(isinstance(e, LanguageAction))
        self.assertEquals('en', e.language)
        self.assertEquals(False, e.only_empty)

    def test_invoke_edit_view(self):
        element = getUtility(IRuleAction,
                             name='sc.contentrules.actions.Language')
        e = LanguageAction()
        editview = getMultiAdapter((e, self.folder.REQUEST),
                                   name=element.editview)
        self.failUnless(isinstance(editview, LanguageEditForm))

    def test_execute(self):
        e = LanguageAction()
        e.language = 'en'
        e.only_empty = False

        ex = getMultiAdapter((self.folder, e,
                             DummyEvent(self.sub_folder)),
                             IExecutable)
        self.assertEquals(True, ex())

        self.assertEquals(self.sub_folder.Language(),
                          e.language)

    def test_execute_only_if_empty(self):
        e = LanguageAction()
        e.language = 'en'
        e.only_empty = True

        ex = getMultiAdapter((self.folder, e,
                             DummyEvent(self.document)),
                             IExecutable)
        self.assertEquals(False, ex())

        self.assertNotEquals(self.document.Language(),
                             e.language)

    def test_execute_empty(self):
        e = LanguageAction()
        e.language = 'en'
        e.only_empty = False

        ex = getMultiAdapter((self.folder, e,
                             DummyEvent(self.document)),
                             IExecutable)
        self.assertEquals(True, ex())

        self.assertEquals(self.document.Language(),
                          e.language)
