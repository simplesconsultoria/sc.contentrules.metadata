# -*- coding:utf-8 -*-
from plone.app.contentrules.rule import Rule
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.contentrules.engine.interfaces import IRuleStorage
from plone.contentrules.rule.interfaces import IExecutable
from plone.contentrules.rule.interfaces import IRuleAction
from sc.contentrules.metadata.actions.contributors import ContributorsAction
from sc.contentrules.metadata.actions.contributors import ContributorsEditForm
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


class TestContributorsAction(unittest.TestCase):

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
        self.document.setContributors(('foo', ))
        self.document.reindexObject()

    def test_registered(self):
        element = getUtility(IRuleAction,
                             name='sc.contentrules.actions.Contributors')
        self.assertEquals('sc.contentrules.actions.Contributors',
                          element.addview)
        self.assertEquals('edit', element.editview)
        self.assertEquals(None, element.for_)
        self.assertEquals(IObjectEvent, element.event)

    def test_invoke_add_view(self):
        element = getUtility(IRuleAction,
                             name='sc.contentrules.actions.Contributors')
        storage = getUtility(IRuleStorage)
        storage[u'foo'] = Rule()
        rule = self.portal.restrictedTraverse('++rule++foo')

        adding = getMultiAdapter((rule, self.portal.REQUEST),
                                 name='+action')
        addview = getMultiAdapter((adding, self.portal.REQUEST),
                                  name=element.addview)

        addview.createAndAdd(data={'contributors': ('bar', ),
                                   'only_empty': False})

        e = rule.actions[0]
        self.failUnless(isinstance(e, ContributorsAction))
        self.assertEquals(('bar', ), e.contributors)
        self.assertEquals(False, e.only_empty)

    def test_invoke_edit_view(self):
        element = getUtility(IRuleAction,
                             name='sc.contentrules.actions.Contributors')
        e = ContributorsAction()
        editview = getMultiAdapter((e, self.folder.REQUEST),
                                   name=element.editview)
        self.failUnless(isinstance(editview, ContributorsEditForm))

    def test_execute(self):
        e = ContributorsAction()
        e.contributors = ('bar', )
        e.only_empty = False

        ex = getMultiAdapter((self.folder, e,
                             DummyEvent(self.sub_folder)),
                             IExecutable)
        self.assertEquals(True, ex())

        self.assertEquals(self.sub_folder.Contributors(),
                          e.contributors)

    def test_execute_only_if_empty(self):
        e = ContributorsAction()
        e.contributors = ('bar', )
        e.only_empty = True

        ex = getMultiAdapter((self.folder, e,
                             DummyEvent(self.document)),
                             IExecutable)
        self.assertEquals(False, ex())

        self.assertNotEquals(self.document.Contributors(),
                             e.contributors)

    def test_execute_empty(self):
        e = ContributorsAction()
        e.contributors = ('bar', )
        e.only_empty = False

        ex = getMultiAdapter((self.folder, e,
                             DummyEvent(self.document)),
                             IExecutable)
        self.assertEquals(True, ex())

        self.assertEquals(self.document.Contributors(),
                          e.contributors)
