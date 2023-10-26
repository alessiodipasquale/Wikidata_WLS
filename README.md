# wikidata-debate 
To quickly set up your Python environment, simply run pip install -r requirements.txt to install all the required dependencies.
# Wikidata Works of art

 The dataset contains 625.110 entities and 4.584.444 statements organized in 12.503 json files. The dataset is available at [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7624784.svg)](https://doi.org/10.5281/zenodo.7624784)
 
The dataset contains data about entities from selected works of art subclasses annotated in wikidata. The whole artworks dataset has been divided into smaller groups in order to obtain an accurate analysis:
- **Audio-Visual heritage** (CHav): This collection holds information about audio-visual materials that have cultural, historical, or artistic value. They include movies, videos, recordings of music or spoken words, and other audio-visual materials that provide a record of a particular event in a specific time or place. The dataset contains 1.251.626 entities and 17.141.394 statements organized in 25.033 json files.
- **Visual heritage** (CHv): This collection holds information about visual artifacts that have cultural, historical, or artistic value. They include paintings, drawings, sculptures, photographs, decorative arts, etc. The dataset contains 1.078.855 entities and 12.850.825 statements organized in 21.579 json files.
- **Textual heritage** (CHt): This collection holds information about written and printed materials that have historical or cultural significance. They include books, manuscripts, letters, and other written documents.
- **Stars** (ANs): This collection holds a random selection of 1.199.950 Wikidata entities (of the 3.3 million existing) belonging to the class `Q523`. The dataset contains 27.470.140 statements in 23.999 json.
- **Galaxies** (ANg): This collection holds a random selection of 1.200.000 Wikidata entities (of the 2 million existing) belonging to the class `Q318`. The dataset contains 14.439.421 statements in 24.000 json files.
- **Random** (R): This dataset comprises 1.159.800 Wikidata entities (starting from a selection of 1.2 million entities from which we removed duplicates) chosen randomly from the most used 100 classes, reflecting the
proportional distribution of entities found in Wikidata. This dataset encompasses 61.798.072 statements distributed across 23.196 JSON files.
# Wikidata patterns to express WLS 

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

| Python File                       |   Usage context  | Description |  
|:---------------------------------:|------------------|---------------|
| `cleanSubject.py`                 | Data acquisition | It parses a json containing all wikidata entities retrieve via SPARQL query and produces an on-purpose string for Wikidata API requests|
| `requestForApi.py`                | Data acquisition | From a list of Wikidata, it requests via Wikidata API all claims related to requested entitites. The output is a folder containing a number of json files with 50 entities and claims each  |
| `data_subgroups_and_clean.ipynb`  | Data acquisition | Creates three subdatasets from culural heritage (CH) data in json files. The output are three folders storing CHt, CHav and CHv data |
| `reduceJsonWeight.py`             | Data acquisition | It runs over all json files stored in a folder and removes indentation. This considerably lowers the weight of the files   |
| `formatSubject.py`                |               |               |
| `mergedAnalysis.py`               |               |               |
| `searchInDataset.py`              | Data analysis | It allows to search claims with a specific properties (independently to the representation method used) |
| `countAsserted.py`                | Data analysis | It counts all asserted statements in a dataset (set of json files stored in sigle folder) |
| `countRanking.py`                 | Data analysis | It counts all ranked statements in a dataset (set of json files stored in sigle folder) |
| `countBlank.py`                   | Data analysis | It counts all null-valued statements in a dataset (set of json files stored in sigle folder)  |
| `countEntities.py`                | Data analysis | It counts all the entities in a dataset (set of json files stored in sigle folder)  |
| `countCategories.py`              | Data analysis | It counts all "instance of" (P31) in a dataset (set of json files stored in sigle folder)  |
| `countNatureCircumstances.py`     | Data analysis | It counts all "nature of statement" (P5102) or "sourcing circumnstances" (P1480) qualified statements in a dataset (set of json files stored in sigle folder)  |
| `countReasonOfDeprecation.py`     | Data analysis | It counts all "reason for deprecation" (P2241) qualified statements in a dataset (set of json files stored in sigle folder)  |
| `countNatureWithDeprecates.py`    | Data analysis | It counts all "reason for deprecation" (P2241) and "nature of statement" (P5102) or "sourcing circumnstances" (P1480) qualified statements in a dataset (set of json files stored in sigle folder)  |
| `countReasonOfPreferred.py`       | Data analysis | It counts all "reason for preferred rank" (P7452) qualified statements in a dataset (set of json files stored in sigle folder) |
| `countProperties.py`              | Data analysis | It counts all properties used in statements in a dataset (set of json files stored in sigle folder) |
| `countTopDeprecatedProperties.py` | Data analysis | It counts the properties that occurr with deprecated statements in a dataset and ranks them by number of occurrences  |
| `countTopNotAssertedProperties.py`| Data analysis | It counts all properties that occurr with asserted statements in a dataset and ranks them by number of occurrences   |
| `countTopQualifiersProperties.py` | Data analysis | It counts all properties that occurr with a qualified statement (P1480, P5102) in a dataset and ranks them by number of occurrences   |
| `countSomevalues.py`              | Data analysis | It counts all properties that occurr with a snaktype "somevalue" in a dataset and ranks them by number of occurrences   |
| `countSomevaluesAsserted.py`      | Data analysis | It counts all properties that occurr with a snaktype "somevalue" and it is asserted in a dataset and ranks them by number of occurrences   |
| `countSomevaluesWithDeprecates.py`| Data analysis | It counts all properties that occurr with a snaktype "somevalue" and deprecated rank in a dataset and ranks them by number of occurrences   |
| `visualisation.ipynb` | Data analysis | It plots a venn3 diagram visualising overlaps of terms in claims in CH dataset qualified with P5102, 1480 and P2241. It also plots a stacked barchart for each dataset (CHv, CHav, CHt, Ag, Ag) with the top 25 most recurrent properties occurring with null-valued statements, non-asserted:normal rank, non-asserted:deprecated rank, qualified statements with P5102 and P1480 |


    
