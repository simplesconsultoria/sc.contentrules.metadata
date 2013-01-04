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
from zope.schema import Choice


VOCAB = 'plone.app.vocabularies.AvailableContentLanguages'

FORM_NAME = _(u"Configure action")

FORM_DESC = _(u'An action that sets language to a content.')


class ILanguageAction(Interface):
    '''Interface for the configurable aspects of a set language action.
       This is also used to create add and edit forms, below.
    '''

    language = Choice(title=_(u'Language'),
                      description=_(u'Select here the language to be applied '
                                    u'to the content item.'),
                      required=True,
                      vocabulary=VOCAB)

    only_empty = Bool(title=_(u"Only if not set"),
                      description=_(u"Apply this only if no language was "
                                    u"set on the content item."),
                      required=False,
                      default=True)


class LanguageAction(SimpleItem):
    """ Stores action settings
    """
    implements(ILanguageAction, IRuleElementData)

    element = 'sc.contentrules.actions.Language'
    language = ''
    only_empty = True

    @property
    def summary(self):
        language = self.language
        only_empty = self.only_empty
        condition = (only_empty and _(u', only if language was not set.') or
                     _(u'.'))
        msg = _(u"Set language ${language}${condition}",
                mapping=dict(language=language, condition=condition))
        return msg


class LanguageActionExecutor(object):
    """ Execute an action
    """
    implements(IExecutable)
    adapts(Interface, ILanguageAction, Interface)

    def __init__(self, context, element, event):
        self.context = context
        self.element = element
        self.event = event

    def __call__(self):
        '''  Apply selected layout to a content item
        '''
        obj = self.event.object
        language = self.element.language
        only_empty = self.element.only_empty
        if not (utils.language_available(obj)):
            return False
        if only_empty:
            if (utils.language_for_object(obj)):
                return False
        return utils.set_language(obj, language)


class LanguageAddForm(AddForm):
    """
    An add form for the Language contentrules action
    """
    form_fields = form.FormFields(ILanguageAction)
    label = _(u"Add set Language content rules action")
    description = FORM_DESC
    form_name = FORM_NAME

    def create(self, data):
        a = LanguageAction()
        form.applyChanges(a, self.form_fields, data)
        return a


class LanguageEditForm(EditForm):
    """
    An edit form for the set Language contentrules action
    """
    form_fields = form.FormFields(ILanguageAction)
    label = _(u"Edit the set Language content rules action")
    description = FORM_DESC
    form_name = FORM_NAME
