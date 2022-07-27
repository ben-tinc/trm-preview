## TOC



## Introduction

* Thesaurus vs controlled vocabulary, taxonomy, ontology etc.



## HTE as basis (?)

* project of the University of Glasgow
* Website: HTE, based on ODE
* specific for English language (but _various kinds_ of English)
* combines rich taxonomy with concrete utterances from ODE


### Access to HTE

* not Open Access
* no API (except crawling the website)
* agreement on re-use


### Access to HTE (cont.)

* two different sets of categories
  * full HTE set, e.g. '01.02.04': "foo" (~144,000 concepts)
  * thematic category set (TC), e.g. 'A01c': "foo" (4,033 concepts)
  * TC is supposed to be used for human queries and visualizations; it is not as readily accessible via the website
* we _only_ have access to the taxonomy data, and _only_ of the TC set!


### TC overview

--> show SKOSMOS



## Data Model


### SKOS

* based on "concepts", identified by URIs
* concepts get various kinds of "labels" in different languages, e.g. "Love"@en
* concepts get connected by hierarchical relations like "narrower", "broader" to form a taxonomy (directed graph, not a tree)
* concepts get connected by non-hierarchical relations to express mappings, e.g. "broadMatch"
* concepts can have "notations" to model traditional signatures e.g. "01.04.02"
* basically everything can have notes attached to it



## Current State


### Read-Only

* HTE dataset has been converted to SKOS
* Skosmos instance available


### we see that

* there are many "top-level" concepts
* some gaps in the hierarchy
* our "big three" are not special in this taxonomy
  * AA: "world"
  * AR: "mind"
  * AY: "society"


### Editable

* VocBench?
* EVOKS?
* vocabseditor?
* other…?



## Challenges
#### (as I see it…)


### Challenges

* Modelling / Extension
* Organizational
* Connection to textual sources