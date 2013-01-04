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
from zope.schema import TextLine
from zope.schema import Tuple


FORM_NAME = _(u"Configure action")

FORM_DESC = _(u'An action that sets creators to a content.')


class ICreatorsAction(Interface):
    '''Interface for the configurable aspects of a set creators action.
       This is also used to create add and edit forms, below.
    '''

    creators = Tuple(title=_(u'Creators'),
                     description=_(u'Persons responsible for creating the '
                                   u'content of this item. Please enter a '
                                   u'list of user names, one per line. The '
                                   u'principal creator should come first.'),
                     value_type=TextLine(),
                     required=False,)

    only_empty = Bool(title=_(u"Only if not set"),
                      description=_(u"Apply this only if no creators was "
                                    u"set on the content item."),
                      required=False,
                      default=True)


class CreatorsAction(SimpleItem):
    """ Stores action settings
    """
    implements(ICreatorsAction, IRuleElementData)

    element = 'sc.contentrules.actions.Creators'
    creators = ''
    only_empty = True

    @property
    def summary(self):
        creators = self.creators
        only_empty = self.only_empty
        condition = (only_empty and _(u', only if creators was not set.') or
                     _(u'.'))
        msg = _(u"Set creators to ${creators}${condition}",
                mapping=dict(creators=','.join(creators),
                             condition=condition))
        return msg


class CreatorsActionExecutor(object):
    """ Execute an action
    """
    implements(IExecutable)
    adapts(Interface, ICreatorsAction, Interface)

    def __init__(self, context, element, event):
        self.context = context
        self.element = element
        self.event = event

    def __call__(self):
        '''  Apply selected layout to a content item
        '''
        obj = self.event.object
        creators = self.element.creators
        only_empty = self.element.only_empty
        if not (utils.creators_available(obj)):
            return False
        if only_empty:
            if (utils.creators_for_object(obj)):
                return False
        return utils.set_creators(obj, creators)


class CreatorsAddForm(AddForm):
    """
    An add form for the Creators contentrules action
    """
    form_fields = form.FormFields(ICreatorsAction)
    label = _(u"Add set Creators content rules action")
    description = FORM_DESC
    form_name = FORM_NAME

    def create(self, data):
        a = CreatorsAction()
        form.applyChanges(a, self.form_fields, data)
        return a


class CreatorsEditForm(EditForm):
    """
    An edit form for the set Creators contentrules action
    """
    form_fields = form.FormFields(ICreatorsAction)
    label = _(u"Edit the set Creators content rules action")
    description = FORM_DESC
    form_name = FORM_NAME
