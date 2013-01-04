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

FORM_DESC = _(u'An action that sets contributors to a content.')

DESC = _(u'The names of people that have contributed to this item. Each '
         u'contributor should  be on a separate line.')


class IContributorsAction(Interface):
    '''Interface for the configurable aspects of a set contributors action.
       This is also used to create add and edit forms, below.
    '''

    contributors = Tuple(title=_(u'Contributors'),
                         description=DESC,
                         value_type=TextLine(),
                         required=False,)

    only_empty = Bool(title=_(u"Only if not set"),
                      description=_(u"Apply this only if no contributors was "
                                    u"set on the content item."),
                      required=False,
                      default=True)


class ContributorsAction(SimpleItem):
    """ Stores action settings
    """
    implements(IContributorsAction, IRuleElementData)

    element = 'sc.contentrules.actions.Contributors'
    contributors = ''
    only_empty = True

    @property
    def summary(self):
        contributors = self.contributors
        only_empty = self.only_empty
        condition = (only_empty and
                     _(u', only if contributors was not set.') or
                     _(u'.'))
        msg = _(u"Set contributors to ${contributors}${condition}",
                mapping=dict(contributors=','.join(contributors),
                             condition=condition))
        return msg


class ContributorsActionExecutor(object):
    """ Execute an action
    """
    implements(IExecutable)
    adapts(Interface, IContributorsAction, Interface)

    def __init__(self, context, element, event):
        self.context = context
        self.element = element
        self.event = event

    def __call__(self):
        '''  Apply selected layout to a content item
        '''
        obj = self.event.object
        contributors = self.element.contributors
        only_empty = self.element.only_empty
        if not (utils.contributors_available(obj)):
            return False
        if only_empty:
            if (utils.contributors_for_object(obj)):
                return False
        return utils.set_contributors(obj, contributors)


class ContributorsAddForm(AddForm):
    """
    An add form for the Contributors contentrules action
    """
    form_fields = form.FormFields(IContributorsAction)
    label = _(u"Add set Contributors content rules action")
    description = FORM_DESC
    form_name = FORM_NAME

    def create(self, data):
        a = ContributorsAction()
        form.applyChanges(a, self.form_fields, data)
        return a


class ContributorsEditForm(EditForm):
    """
    An edit form for the set Contributors contentrules action
    """
    form_fields = form.FormFields(IContributorsAction)
    label = _(u"Edit the set Contributors content rules action")
    description = FORM_DESC
    form_name = FORM_NAME
