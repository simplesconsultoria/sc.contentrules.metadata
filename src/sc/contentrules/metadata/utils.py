# -*- coding:utf-8 -*-
from Acquisition import aq_base


def subject_available(obj):
    ''' '''
    return (hasattr(aq_base(obj), 'setSubject') or
            hasattr(aq_base(obj), 'subject') or
            hasattr(aq_base(obj), 'subjects'))


def subject_for_object(obj):
    ''' '''
    subject = []
    if hasattr(aq_base(obj), 'Subject'):
        subject = obj.Subject()
    elif hasattr(aq_base(obj), 'subject'):
        subject = obj.subject
    elif hasattr(aq_base(obj), 'subjects'):
        subject = obj.subjects
    return subject


def set_subject(obj, subject):
    ''' '''
    if hasattr(aq_base(obj), 'setSubject'):
        obj.setSubject(subject)
    elif hasattr(aq_base(obj), 'subject'):
        obj.subject = subject
    elif hasattr(aq_base(obj), 'subjects'):
        obj.subjects = subject
    return True


def exclude_from_nav_available(obj):
    ''' '''
    return (hasattr(aq_base(obj), 'exclude_from_nav'))


def set_exclude_from_nav(obj, exclude):
    ''' '''
    if hasattr(aq_base(obj), 'setExcludeFromNav'):
        obj.setExcludeFromNav(exclude)
    elif hasattr(aq_base(obj), 'exclude_from_nav'):
        obj.exclude_from_nav = exclude
    return True


def language_available(obj):
    ''' '''
    return (hasattr(aq_base(obj), 'setLanguage') or
            hasattr(aq_base(obj), 'language'))


def language_for_object(obj):
    ''' '''
    language = ''
    if hasattr(aq_base(obj), 'Language'):
        language = obj.Language()
    elif hasattr(aq_base(obj), 'language'):
        language = obj.language
    return language


def set_language(obj, language):
    ''' '''
    if hasattr(aq_base(obj), 'setLanguage'):
        obj.setLanguage(language)
    elif hasattr(aq_base(obj), 'language'):
        obj.language = language
    return True


def rights_available(obj):
    ''' '''
    return (hasattr(aq_base(obj), 'setRights') or
            hasattr(aq_base(obj), 'rights'))


def rights_for_object(obj):
    ''' '''
    rights = ''
    if hasattr(aq_base(obj), 'Rights'):
        rights = obj.Rights()
    elif hasattr(aq_base(obj), 'rights'):
        rights = obj.rights
    return rights


def set_rights(obj, rights):
    ''' '''
    if hasattr(aq_base(obj), 'setRights'):
        obj.setRights(rights)
    elif hasattr(aq_base(obj), 'rights'):
        obj.rights = rights
    return True


def creators_available(obj):
    ''' '''
    return (hasattr(aq_base(obj), 'setCreators') or
            hasattr(aq_base(obj), 'creators'))


def creators_for_object(obj):
    ''' '''
    creators = ''
    if hasattr(aq_base(obj), 'Creators'):
        creators = obj.Creators()
    elif hasattr(aq_base(obj), 'creators'):
        creators = obj.creators
    return creators


def set_creators(obj, creators):
    ''' '''
    if hasattr(aq_base(obj), 'setCreators'):
        obj.setCreators(creators)
    elif hasattr(aq_base(obj), 'creators'):
        obj.creators = creators
    return True


def contributors_available(obj):
    ''' '''
    return (hasattr(aq_base(obj), 'setContributors') or
            hasattr(aq_base(obj), 'contributors'))


def contributors_for_object(obj):
    ''' '''
    contributors = ''
    if hasattr(aq_base(obj), 'Contributors'):
        contributors = obj.Contributors()
    elif hasattr(aq_base(obj), 'contributors'):
        contributors = obj.contributors
    return contributors


def set_contributors(obj, contributors):
    ''' '''
    if hasattr(aq_base(obj), 'setContributors'):
        obj.setContributors(contributors)
    elif hasattr(aq_base(obj), 'contributors'):
        obj.contributors = contributors
    return True
