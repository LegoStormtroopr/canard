Canard Question Module Editor
======

Canard is a [what-you-see-is-what-you-mean](http://en.wikipedia.org/wiki/WYSIWYM) editor that allows a questionnaire
designer to describe their intent behind a data collection instrument, but also allows them to see a real-time live
example of what that specification may look like when presented to a respondent.

Canard also acts a a prototype tool for illustrating (and testing) the principles of Structured
Questionnaire Design, using the [Simple Questionnaire Building Language](http://sqbl.org) as its
management format. By using the cutdown SQBL format, Canard remains agile requiring network connectivity
only when connecting modules together, while allowing an entire question module to be captured within a single document.

A series of [tutorial videos](http://bit.ly/CanardVideos) are available on youtube showing how to use the software.


Features
-------------
Currently functional in this release:
 - Dynamic text and word substitutions in question text and statements
 - Nested branching and complex routing within surveys
 - Three types of basic response type:
  - Text - with optional enforcement of minimum and maximum response length
  - Number - with optional enforcement of minimum and maximum values, with required step values
  - Codelists - with the ability to indicate a minimum and maximum number of choices
 - While also allowing for complex response types:
  - Question Groups - allow for tightly linked questions with different responses to be brought together.
  - Individual questions can have subquestions and multiple responses to capture complex lists and grids of responses quickly.
 - Live preview of question routing and example form instances using Graphviz and XForms.
 - Plug-in support to extend *import and export* functionality
  - This release includes plugins for [DDI3.1](http://www.ddialliance.org/Specification/DDI-Lifecycle/3.1/) import and export
 - **Multilingual** settings to insert and manage multiple languages in the same question module 

How to install (Windows)
-------------
1. Download the above executable
2. Extract to a location of your choosing.
3. (Optional) [Install Graphviz](http://www.graphviz.org/), however without this installed the flowchart panel be able to provide illustrations of the logical routing.

How to Install (Linux & Mac)
-------------
Coming soon!

Tutorials
--------------
[A playlist of Canard tutorial videos is available on Youtube](http://bit.ly/CanardVideos)

Screenshots
--------------
A word substitution providing dynamic text in question.
![Screen shot of word substitutions](http://i.imgur.com/EO842ry.png "Word substitutions")
