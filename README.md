# wikidata-debate
 The dataset contains 625.110 entities and 4.584.444 statements organized in 12.503 json files. The dataset is available at [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7624784.svg)](https://doi.org/10.5281/zenodo.7624784)
 

# Wikidata Works of art

The dataset contains data about entities from selected works of art subclasses annotated in wikidata. The whole artworks dataset has been divided into smaller groups in order to obtain an accurate analysis:
- **Audio-Visual heritage** (CHav): This collection holds information about audio-visual materials that have cultural, historical, or artistic value. They include movies, videos, recordings of music or spoken words, and other audio-visual materials that provide a record of a particular event in a specific time or place. The dataset contains 1.251.626 entities and 17.141.394 statements organized in 25.033 json files.
- **Visual heritage** (CHv): This collection holds information about visual artifacts that have cultural, historical, or artistic value. They include paintings, drawings, sculptures, photographs, decorative arts, etc. The dataset contains 1.078.855 entities and 12.850.825 statements organized in 21.579 json files.
- **Textual heritage** (CHt): This collection holds information about written and printed materials that have historical or cultural significance. They include books, manuscripts, letters, and other written documents.
- **Stars** (As): This collection holds a random selection of 1.199.950 Wikidata entities (of the 3.3 million existing) belonging to the class `Q523`. The dataset contains 27.470.140 statements in 23.999 json.
- **Galaxies** (Ag): This collection holds a random selection of 1.200.000 Wikidata entities (of the 2 million existing) belonging to the class `Q318`. The dataset contains 14.439.421 statements in 24.000 json files.

# Parameters of the Analysis

## Ranked statements
Competing statements are represented via a ranking mechanism (e.g., Preferred, Normal and Deprecated). Individual statements are not actually asserted, but an extra triple is added those that are deemed true. For example, the painting “Madonna with the Blue Diadem” (`Q738038`) has been attributed to Raphael (non asserted statement, ranked as normal) and Gianfrancesco Penni (asserted statement, ranked as preferred and additionally asserted). 

### Ranked statements with qualifiers
- Deprecated ranked statements which have been annotated with "reason for deprecation" (`pq:P2241`) qualifier. This parameter can tell us why the community decree that an information is not accepted anymore.
- Preferred ranked statements which have been annotated with "reason for " (`pq:P7452`). This parameter can tell us why the community decree that an information is better than the others. 

## Statements with an uncertain qualifier 
Statements, independently of rank, can be decorated with an additional triple using a specific predicate in the role of qualifier, to annotate its contextual information. We selected those annotated terms which mark uncertainty or debate (e.g. debated, hypothesis, possibly).

- **“Nature of statements” qualifiers**. Predicate pq:P5102 marks the nature of a statement. For example, the painting “Abstract Speed + Sound” (`Q19882431`) by Giacomo Balla is deemed to be possibly part of a triptych.  
- **"Sourcing circumstances" qualifiers**. As in the previous case, statements can be annotated with a sourcing circumstance (`pq:P1480`).

## Null-valued objects
A statement can be associated with a blank node. This is meant to imply that the statement is associated with an unknown value, rather than a missing statement. For example, “Missal for the use of the ecclesiastics of Clermont' (`Q113302686`), an illuminated manuscript from the 14th century, has been recorded with both an unknown creator and author.

# Scripts

Below is provided a description of each python file which has been used to perform the analysis.

| Python File                       |   Description |  
|-----------------------------------|:-------------:|
| `cleanSubject.py`                 |  left-aligned |
| `countAsserted.py`                |  left-aligned |
| `countBlank.py`                   |    centered   |
| `countEntities.py`                | right-aligned |
| `cleanSubject.py`                 |  left-aligned |
| `countNatureCircumstances.py`     |  left-aligned |
| `countNatureWithDeprecates.py`    |    centered   |
| `countReasonOfPreferred.py`       | right-aligned |
| `countProperties.py`              | right-aligned |
| `countReasonOfDeprecation.py`     |  left-aligned |
| `countTopDeprecatedProperties.py` |  left-aligned |
| `countTopNotAssertedProperties.py`|    centered   |
| `countTopQualifiersProperties.py` | right-aligned |
| `formatSubject.py`                |  left-aligned |
| `mergedAnalysis.py`               |  left-aligned |
| `reduceJsonWeight.py`             |    centered   |
| `requestForApi.py`                | right-aligned |
| `searchInDataset.py`              | right-aligned |
    
