reStructuredText examples
===========================

These examples use standard Sphinx directives. Each source listing is followed
by its rendered result. Markdown equivalents appear in :doc:`usage`.

Caption, reference, and accessible label
------------------------------------------

.. code-block:: rst

   .. mermaid:: examples/states.mmd
      :caption: Document review states
      :name: review-states
      :alt: A draft moves to review, then returns for revision or is published.
      :align: center

   See :ref:`review-states`.

.. mermaid:: examples/states.mmd
   :caption: Document review states
   :name: review-states
   :alt: A draft moves to review, then returns for revision or is published.
   :align: center

See :ref:`review-states`.

A fixed direction with zoom controls
--------------------------------------

.. code-block:: rst

   .. mermaid::
      :options: {autoDirection: false, fontSize: 18}
      :zoom: {always: true, maxScale: 4, labels: {zoomIn: Enlarge}}
      :width: 80%
      :align: center

      flowchart LR
          Draft --> Review --> Published

.. mermaid::
   :options: {autoDirection: false, fontSize: 18}
   :zoom: {always: true, maxScale: 4, labels: {zoomIn: Enlarge}}
   :width: 80%
   :align: center

   flowchart LR
       Draft --> Review --> Published

A regular code block
----------------------

.. code-block:: rst

   .. code-block:: mermaid

      flowchart TD
          Source --> Build --> Preview

.. code-block:: mermaid

   flowchart TD
       Source --> Build --> Preview

The Pele directive alias
--------------------------

.. code-block:: rst

   .. pele::
      :title: Review decision
      :config: {flowchart: {nodeSpacing: 50}}
      :class: review-diagram

      flowchart TD
          Review{Approved?} -->|Yes| Publish
          Review -->|No| Revise

.. pele::
   :title: Review decision
   :config: {flowchart: {nodeSpacing: 50}}
   :class: review-diagram

   flowchart TD
       Review{Approved?} -->|Yes| Publish
       Review -->|No| Revise
