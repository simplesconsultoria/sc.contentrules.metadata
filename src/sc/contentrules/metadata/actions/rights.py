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
from zope.schema import Text


FORM_NAME = _(u"Configure action")

FORM_DESC = _(u'An action that sets rights to a content.')


class IRightsAction(Interface):
    '''Interface for the configurable aspects of a set rights action.
       This is also used to create add and edit forms, below.
    '''

    rights = Text(title=_(u'Rights'),
                  description=_(u'Inform the copyright statement or other '
                                u'rights information on this item'),
                  required=True)

    only_empty = Bool(title=_(u"Only if not set"),
                      description=_(u"Apply this only if no rights was "
                                    u"set on the content item."),
                      required=False,
                      default=True)


class RightsAction(SimpleItem):
    """ Stores action settings
    """
    implements(IRightsAction, IRuleElementData)

    element = 'sc.contentrules.actions.Rights'
    rights = ''
    only_empty = True

    @property
    def summary(self):
        rights = self.rights
        only_empty = self.only_empty
        condition = (only_empty and _(u', only if rights was not set.') or
                     _(u'.'))
        msg = _(u"Set rights '${rights}'${condition}",
                mapping=dict(rights=rights, condition=condition))
        return msg


class RightsActionExecutor(object):
    """ Execute an action
    """
    implements(IExecutable)
    adapts(Interface, IRightsAction, Interface)

    def __init__(self, context, element, event):
        self.context = context
        self.element = element
        self.event = event

    def __call__(self):
        '''  Apply selected layout to a content item
        '''
        obj = self.event.object
        rights = self.element.rights
        only_empty = self.element.only_empty
        if not (utils.rights_available(obj)):
            return False
        if only_empty:
            if (utils.rights_for_object(obj)):
                return False
        return utils.set_rights(obj, rights)


class RightsAddForm(AddForm):
    """
    An add form for the Rights contentrules action
    """
    form_fields = form.FormFields(IRightsAction)
    label = _(u"Add set Rights content rules action")
    description = FORM_DESC
    form_name = FORM_NAME

    def create(self, data):
        a = RightsAction()
        form.applyChanges(a, self.form_fields, data)
        return a


class RightsEditForm(EditForm):
    """
    An edit form for the set Rights contentrules action
    """
    form_fields = form.FormFields(IRightsAction)
    label = _(u"Edit the set Rights content rules action")
    description = FORM_DESC
    form_name = FORM_NAME
