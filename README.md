Canard Question Module Editor
======

Canard is a [what-you-see-is-what-you-mean](http://en.wikipedia.org/wiki/WYSIWYM) questionnaire application that allows researchers and questionnaire
designers to describe the specification of data collection instrument, while showing a real-time live
example of what a generated questionnaire may look like when presented to a respondent.

Canard is able to provide quick-prototyping for questionnaires and surveys by implementing [the principles of Structured
Questionnaire Design](http://sqbl.org/wiki/index.php/Structured_Questionnaire_Design). Internally, Canard uses the [Simple Questionnaire Building Language](http://sqbl.org) as its internal data model, while also conforming to the XML standards of the Data Documentation Initiative. By using the simplified SQBL format, Canard remains agile requiring network connectivity
only when connecting modules together, while allowing an entire question module to be captured within a single document.

**A series of [tutorial videos](http://bit.ly/CanardVideos) are available on youtube showing how to use the software.**


Current features
-------------
 - Dynamic text and word substitutions in question text and statements
 - Nested branching and complex routing within surveys
 - Six types of basic response type:
  - Text - with optional enforcement of minimum and maximum response length
  - Number - with optional enforcement of minimum and maximum values, with required step values
  - Codelists - with the ability to indicate a minimum and maximum number of choices
  - Binary (yes/no) - for simple presentation of yes/no, on/off response options.
  - Date - with support for allowed date ranges.
  - Time - with support for allowed time ranges.
 - Grouping for complex response types:
  - Question Groups - allow for tightly linked questions with different responses to be brought together.
  - Subquestions to support repeated capture of similar responses
  - Multiple responses against a single question
  - Combinations of subquestions and multiple responses to capture **complex question grids**.
 - Live preview of question routing and example form instances using Graphviz and XForms.
 - XSLT and Python Plug-in support to extend *import and export* functionality
  - This release includes plugins for:
   - [DDI3.1 and DDI3.2](http://www.ddialliance.org/Specification/DDI-Lifecycle/3.1/) import and export
   - The [ACSPRI queXML format](https://surveys.acspri.org.au/quexmltools/) and the [LimeSurvey import format](http://limesurvey.org)
   - The [Triple-S Survey format](http://www.triple-s.org)
 - Multilingual support for managing multiple languages in the same question module.

How to install (Windows)
-------------
1. Download the [most current release](http://bit.ly/canard_releases)
2. Extract to a location of your choosing.
3. (Optional) [Install Graphviz](http://www.graphviz.org/), however without this installed the flowchart panel be able to provide illustrations of the logical routing.

How to Install (Ubuntu 14.04)
-------------

```
sudo apt-get install pyqt4-dev-tools build-essential python-pygraphviz git
git clone https://github.com/LegoStormtroopr/canard.git
cd canard
make
git submodule add https://github.com/LegoStormtroopr/sqbl-schema.git
ln -s sqbl-schema/Schemas/ sqbl
git submodule add -f https://github.com/LegoStormtroopr/roxy-sqbl-instrument-creator.git roxy
python canard_main.py
```

How to Install (Mac)
-------------
Coming soon!

Tutorials
--------------
[A playlist of Canard tutorial videos is available on Youtube](http://bit.ly/CanardVideos)

Screenshots
--------------
A word substitution providing dynamic text in question.
![Screen shot of word substitutions](http://i.imgur.com/EO842ry.png "Word substitutions")
