****************************************************************************
Content Rules: Metadata Conditions and Actions
****************************************************************************

.. contents:: Content
   :depth: 2

Overview
--------

**Content Rules: Metadata Conditions and Actions** (sc.contentrules.metadata) 
package provides a set of content rule conditions and actions to deal with
content item metadata.

This package is tested with Travis CI:

.. image:: https://secure.travis-ci.org/simplesconsultoria/sc.contentrules.metadata.png
    :target: http://travis-ci.org/simplesconsultoria/sc.contentrules.metadata


Actions
---------

This package provides the following content rules actions:

Set Tags
^^^^^^^^^^^^^^^^^^^

Used to set Tags (Keywords, Subject) on a content item. This action relies
on a vocabulary of already used Tags so the user can select the ones to be 
applied on the content item.

Exclude from navigation
^^^^^^^^^^^^^^^^^^^^^^^^

Exclude -- or show -- a content item from navigation.


Set Language
^^^^^^^^^^^^^^^^^^^^^^^^

Content rule action to set the Language metadata field on a content item.

Set Rights
^^^^^^^^^^^^^^^^^^^^^^^^

Content rule action to set the Rights metadata field on a content item. i.e.: 
"Copyleft 2013 - Radio del Sur"

Set Creators
^^^^^^^^^^^^^^^^^^^^^^^^

Content rule action to set the Creators metadata field on a content item. i.e.: 
"Lawrence Lessig"

Set Contributors
^^^^^^^^^^^^^^^^^^^^^^^^

Content rule action to set the Contributors metadata field on a content item.
i.e.:  "et al."

Conditions
------------

This package provides the following content rules conditions:

Tag
^^^^^^^^^^^^^^^^^^^^^^^^

Content rule condition that will apply only when the current content item 
contains the selected Tags.


Requirements
------------

    * Plone 4.1.x and above (http://plone.org/products/plone)
