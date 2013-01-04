# -*- coding:utf-8 -*-
from Acquisition import aq_inner
from OFS.SimpleItem import SimpleItem
from plone.app.contentrules import PloneMessageFactory as _
from plone.app.contentrules.browser.formhelper import AddForm
from plone.app.contentrules.browser.formhelper import EditForm
from plone.contentrules.rule.interfaces import IExecutable
from plone.contentrules.rule.interfaces import IRuleElementData
from sc.contentrules.metadata import utils
from zope.component import adapts
from zope.formlib import form
from zope.interface import implements
from zope.interface import Interface
from zope.schema import Choice
from zope.schema import Set

VOCAB = 'plone.app.vocabularies.Keywords'

FORM_NAME = _(u"Configure condition")

FORM_DESC = _(u'A tag condition makes the rule apply only to contents with '
              u'any of the selected tags. If no tag is selected the rule '
              u'will apply to contents without tags applied to them.')


class ISubjectCondition(Interface):
    '''Interface for the configurable aspects of a Tag condition.
       This is also used to create add and edit forms, below.
    '''

    subject = Set(title=_(u'Tags'),
                  description=_(u'Tags to check for. Leave it blank '
                                u'to check for contents without any '
                                u'tag set'),
                  required=False,
                  value_type=Choice(vocabulary=VOCAB))


class SubjectCondition(SimpleItem):
    '''The actual persistent implementation of the Tag condition element.
    '''
    implements(ISubjectCondition, IRuleElementData)

    subject = []
    element = "sc.contentrules.conditions.Subject"

    @property
    def summary(self):
        subject = self.subject
        if not subject:
            msg = _(u"No tags selected")
        else:
            msg = _(u"Tags contains ${tags}",
                    mapping=dict(tags=" or ".join(subject)))
        return msg


class SubjectConditionExecutor(object):
    """The executor for this condition.

    This is registered as an adapter in configure.zcml
    """
    implements(IExecutable)
    adapts(Interface, ISubjectCondition, Interface)

    def __init__(self, context, element, event):
        self.context = context
        self.element = element
        self.event = event

    def __call__(self):
        expected = self.element.subject
        obj = aq_inner(self.event.object)

        if not (utils.subject_available(obj)):
            return False

        subject = utils.subject_for_object(obj)
        if not expected:
            return not (expected or subject)
        intersection = set(expected).intersection(subject)
        return intersection and True or False


class SubjectAddForm(AddForm):
    """An add form for Tag conditions.
    """
    form_fields = form.FormFields(ISubjectCondition)
    label = _(u'Add Tag Condition')
    description = FORM_DESC
    form_name = FORM_NAME

    def create(self, data):
        c = SubjectCondition()
        form.applyChanges(c, self.form_fields, data)
        return c


class SubjectEditForm(EditForm):
    """An edit form for Tag conditions
    """
    form_fields = form.FormFields(ISubjectCondition)
    label = _(u"Edit Tag Condition")
    description = FORM_DESC
    form_name = FORM_NAME
