# -*- coding: utf-8 -*-
from Acquisition import aq_parent
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
from zope.schema import Choice
from zope.schema import Set


VOCAB = 'plone.app.vocabularies.Keywords'

FORM_NAME = _(u"Configure action")

FORM_DESC = _(u'An action that applies Tags to a content.')


class ISubjectAction(Interface):
    '''Interface for the configurable aspects of a set Tag action.
       This is also used to create add and edit forms, below.
    '''

    same_as_parent = Bool(title=_(u"Use Tags from parent object"),
                          description=_(u"Select this to use Tags as defined "
                                        u"in the parent object. If this "
                                        u"option is selected this action "
                                        u"ignores the following field."))

    subject = Set(title=_(u'Tags'),
                  description=_(u'Tags to check for. Leave it blank '
                                u'to check for contents without any '
                                u'tag set'),
                  required=False,
                  value_type=Choice(vocabulary=VOCAB))


class SubjectAction(SimpleItem):
    """ Stores action settings
    """
    implements(ISubjectAction, IRuleElementData)

    element = 'sc.contentrules.actions.Subject'
    same_as_parent = False
    subject = []

    @property
    def summary(self):
        same_as_parent = self.same_as_parent
        subject = self.subject
        if same_as_parent:
            msg = _(u"Apply tags from parent object.")
        else:
            msg = _(u"Apply tags ${tags}",
                    mapping=dict(tags=", ".join(subject)))
        return msg


class SubjectActionExecutor(object):
    """ Execute an action
    """
    implements(IExecutable)
    adapts(Interface, ISubjectAction, Interface)

    def __init__(self, context, element, event):
        self.context = context
        self.element = element
        self.event = event

    def __call__(self):
        '''  Apply selected layout to a content item
        '''
        obj = self.event.object
        same_as_parent = self.element.same_as_parent
        subject = self.element.subject
        if not (utils.subject_available(obj)):
            return False
        if same_as_parent:
            parent = aq_parent(obj)
            if not (utils.subject_available(parent)):
                return False
            subject = utils.subject_for_object(parent)
        return utils.set_subject(obj, subject)


class SubjectAddForm(AddForm):
    """
    An add form for the Tags contentrules action
    """
    form_fields = form.FormFields(ISubjectAction)
    label = _(u"Add set Tags content rules action")
    description = FORM_DESC
    form_name = FORM_NAME

    def create(self, data):
        a = SubjectAction()
        form.applyChanges(a, self.form_fields, data)
        return a


class SubjectEditForm(EditForm):
    """
    An edit form for the set Tags contentrules action
    """
    form_fields = form.FormFields(ISubjectAction)
    label = _(u"Edit the set Tags content rules action")
    description = FORM_DESC
    form_name = FORM_NAME
