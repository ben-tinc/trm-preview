## TOC

* Definition: ”Thesauri“
* HTE as a basis
* Data Model
* Current State
* Challenges
* The Way Forward



## Introduction

* Thesaurus vs controlled vocabulary, taxonomy, ontology etc.

<figure>
<img alt="comparison of thesaurus to other types of controlled vocabularies" src="./img/Controlled-vocabulary-types-chart-thesauri.png">
<figcaption>Source: <a href="https://www.hedden-information.com/what-is-a-thesaurus-and-what-is-it-good-for/">https://www.hedden-information.com/what-is-a-thesaurus-and-what-is-it-good-for/</a>.</figcaption>
</figure>



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
  * full HTE set, e.g. '01.04.02': "Anthropocentrism" (~144,000 concepts)
  * thematic category set (TC), e.g. 'AD01': "Science of mankind" (4,033 concepts)
  * TC is supposed to be used for human queries and visualizations; it is not as readily accessible via the website
* we _only_ have access to the taxonomy data, and _only_ of the TC set!


<!-- .slide: data-background-iframe="https://ht.ac.uk/category/#id=39622" -->

Notes: The TC mapping is not easily searchable in the web interface, but it is visible by using the detail view of a full HTE category.
While in theory the TC set of categories seems like a good fit for our project, in practice I found it to be _weird_. TODO: show cases of weirdness!



## Data Model


### SKOS

<div style="display: grid; grid-template-columns: 1fr 1fr;">
<div class="list">
<ul>
<li class="fragment" data-fragment-index="1">based on <b>concepts</b>, identified by URIs</li> 
<li class="fragment" data-fragment-index="2">concepts get various kinds of <b>labels</b> in different languages, e.g. <em>"Love"@en</em></li>
<li class="fragment" data-fragment-index="3">concepts get connected by <b>hierarchical relations</b> like <em>"narrower"</em> to form a taxonomy (directed graph, not a tree)</li>
<li class="fragment" data-fragment-index="4">concepts get connected by <b>non-hierarchical relations</b> to express mappings, e.g. <em>"closeMatch"</em></li>
<li class="fragment" data-fragment-index="5">concepts can have <b>notations</b> to model traditional signatures e.g. <em>"01.04.02"</em></li>
<li class="fragment" data-fragment-index="6">basically everything can have <b>notes</b> attached to it</li>
</ul>
</div>
<div class="graphic">
<div class="r-stack">
  <img alt="SKOS Concepts" src="./img/skos-model-1.png" class="fragment" data-fragment-index="1"/>
  <img alt="SKOS Labels" src="./img/skos-model-2.png" class="fragment" data-fragment-index="2"/>
  <img alt="SKOS Hierarchy" src="./img/skos-model-3.png" class="fragment" data-fragment-index="3"/>
  <img alt="SKOS Mappings" src="./img/skos-model-4.png" class="fragment" data-fragment-index="4"/>
  <img alt="SKOS Notations" src="./img/skos-model-5.png" class="fragment" data-fragment-index="5"/>
</div>
</div>
</div>

Notes: We see that while "Emotion" is parent of "Love" in HTE, in TC they are sibling elements. The TC concept "AU":"Emotion" is not mapped by the HTE editors.


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



## The Way Forward

