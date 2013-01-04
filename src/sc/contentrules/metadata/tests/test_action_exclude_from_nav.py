# -*- coding:utf-8 -*-
from plone.app.contentrules.rule import Rule
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.contentrules.engine.interfaces import IRuleStorage
from plone.contentrules.rule.interfaces import IExecutable
from plone.contentrules.rule.interfaces import IRuleAction
from Products.CMFCore.PortalContent import PortalContent
from sc.contentrules.metadata.actions.navigation import ExcludeFromNavAction
from sc.contentrules.metadata.actions.navigation import ExcludeFromNavEditForm
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


class TestExcludeFromNavAction(unittest.TestCase):

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

    def test_registered(self):
        element = getUtility(IRuleAction,
                             name='sc.contentrules.actions.ExcludeFromNav')
        self.assertEquals('sc.contentrules.actions.ExcludeFromNav',
                          element.addview)
        self.assertEquals('edit', element.editview)
        self.assertEquals(None, element.for_)
        self.assertEquals(IObjectEvent, element.event)

    def test_invoke_add_view(self):
        element = getUtility(IRuleAction,
                             name='sc.contentrules.actions.ExcludeFromNav')
        storage = getUtility(IRuleStorage)
        storage[u'foo'] = Rule()
        rule = self.portal.restrictedTraverse('++rule++foo')

        adding = getMultiAdapter((rule, self.portal.REQUEST),
                                 name='+action')
        addview = getMultiAdapter((adding, self.portal.REQUEST),
                                  name=element.addview)

        addview.createAndAdd(data={'exclude': False})

        e = rule.actions[0]
        self.failUnless(isinstance(e, ExcludeFromNavAction))
        self.assertEquals(False, e.exclude)

    def test_invoke_edit_view(self):
        element = getUtility(IRuleAction,
                             name='sc.contentrules.actions.ExcludeFromNav')
        e = ExcludeFromNavAction()
        editview = getMultiAdapter((e, self.folder.REQUEST),
                                   name=element.editview)
        self.failUnless(isinstance(editview, ExcludeFromNavEditForm))

    def test_execute_excluding(self):
        e = ExcludeFromNavAction()
        e.exclude = True

        ex = getMultiAdapter((self.folder, e,
                             DummyEvent(self.sub_folder)),
                             IExecutable)
        self.assertEquals(True, ex())

        self.assertEquals(self.sub_folder.exclude_from_nav(),
                          e.exclude)
