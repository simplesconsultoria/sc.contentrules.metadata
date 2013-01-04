# -*- coding: utf-8 -*-
from OFS.SimpleItem import SimpleItem
from plone.app.contentrules.browser.formhelper import AddForm
from plone.app.contentrules.browser.formhelper import EditForm
from plone.contentrules.rule.interfaces import IExecutable
from plone.contentrules.rule.interfaces import IRuleElementData
from sc.contentrules.metadata import MessageFactory as _
from sc.contentrules.metadata import utils
from zope.component import adapts
from zope.formlib import form
from zope.interface import implements
from zope.interface import Interface
from zope.schema import Bool


FORM_NAME = _(u"Configure action")

FORM_DESC = _(u'An action that excludes contents from navigation.')


class IExcludeFromNavAction(Interface):
    '''Interface for the configurable aspects of exclude from navigation
       action.
       This is also used to create add and edit forms, below.
    '''

    exclude = Bool(title=_(u"Exclude content from navigation"),
                   description=_(u"If checked the content will not be "
                                 u"listed in portal navigation elements."))


class ExcludeFromNavAction(SimpleItem):
    """ Stores action settings
    """
    implements(IExcludeFromNavAction, IRuleElementData)

    element = 'sc.contentrules.actions.ExcludeFromNav'
    exclude = False

    @property
    def summary(self):
        exclude = self.exclude
        if exclude:
            msg = _(u"Exclude content object from navigation.")
        else:
            msg = _(u"Show content object in navigation.")
        return msg


class ExcludeFromNavActionExecutor(object):
    """ Execute an action
    """
    implements(IExecutable)
    adapts(Interface, IExcludeFromNavAction, Interface)

    def __init__(self, context, element, event):
        self.context = context
        self.element = element
        self.event = event

    def __call__(self):
        '''  Apply selected layout to a content item
        '''
        obj = self.event.object
        exclude = self.element.exclude
        if not (utils.exclude_from_nav_available(obj)):
            return False
        return utils.set_exclude_from_nav(obj, exclude)


class ExcludeFromNavAddForm(AddForm):
    """
    An add form for the exclude from navigation contentrules action
    """
    form_fields = form.FormFields(IExcludeFromNavAction)
    label = _(u"Add an exclude from navigation content rules action")
    description = FORM_DESC
    form_name = FORM_NAME

    def create(self, data):
        a = ExcludeFromNavAction()
        form.applyChanges(a, self.form_fields, data)
        return a


class ExcludeFromNavEditForm(EditForm):
    """
    An edit form for the exclude from navigation contentrules action
    """
    form_fields = form.FormFields(IExcludeFromNavAction)
    label = _(u"Edit an exclude from navigation content rules action")
    description = FORM_DESC
    form_name = FORM_NAME
