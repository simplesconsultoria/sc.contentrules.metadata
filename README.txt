****************************************************************************
Content Rules: Metadata Conditions and Actions
****************************************************************************

.. contents:: Content
   :depth: 2

Life, the Universe, and Everything
----------------------------------

**Content Rules: Metadata Conditions and Actions** (sc.contentrules.metadata) 
package provides a set of content rule conditions and actions to deal with
content item metadata.

Don't Panic
-----------

Actions
^^^^^^^

This package provides the following content rules actions:

Set Tags
++++++++

Used to set Tags (Keywords, Subject) on a content item. This action relies
on a vocabulary of already used Tags so the user can select the ones to be 
applied on the content item.

Exclude from navigation
+++++++++++++++++++++++

Exclude -- or show -- a content item from navigation.

Set Language
++++++++++++

Content rule action to set the Language metadata field on a content item.

Set Rights
++++++++++

Content rule action to set the Rights metadata field on a content item. i.e.: 
"Copyleft 2013 - Radio del Sur"

Set Creators
++++++++++++

Content rule action to set the Creators metadata field on a content item. i.e.: 
"Lawrence Lessig"

Set Contributors
++++++++++++++++

Content rule action to set the Contributors metadata field on a content item.
i.e.:  "et al."

Conditions
^^^^^^^^^^

This package provides the following content rules conditions:

Tag
+++

Content rule condition that will apply only when the current content item 
contains the selected Tags.

Mostly Harmless
---------------

.. image:: https://secure.travis-ci.org/simplesconsultoria/sc.contentrules.metadata.png
    :target: http://travis-ci.org/simplesconsultoria/sc.contentrules.metadata

Got an idea? Found a bug? Let us know by `opening a support ticket`_.

.. _`opening a support ticket`: https://github.com/simplesconsultoria/sc.contentrules.metadata/issues
