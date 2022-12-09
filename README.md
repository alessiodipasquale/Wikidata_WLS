# wikidata-debate
JSONs and Dataset: https://liveunibo-my.sharepoint.com/:f:/g/personal/alessio_dipasquale_studio_unibo_it/EqqYGoYMb7JEslVbixKa2P8ByGGcCPiHsz_-i0JL84Mb_g?e=q8O0Ef


# Wikidata Works of art

The dataset contains data about entities from selected works of art subclasses annotated in wikidata. The whole artworks dataset has been divided into smaller groups in order to obtain an accurate analysis:
- Visual heritage: containting painting, scuplture, decorative arts, drawing, prints
- Textual heritage: containing literary works, manuscripts, maps, theatrical plays
- Pop culture heritage: containing movies, music, tv series
- 
|            | Visual    | Textal  | Pop       | Total     |
|------------|-----------|---------|-----------|-----------|
| Entities   | 1'075'935 | 623'414 | 1'250'917 | 2,950,266 |
| Statements |           |         |           |           |
| Classes    |           |         |           |           |

# Parameters of the Analysis

## Ranked statements
Competing statements are represented via a ranking mechanism (e.g., Preferred, Normal and Deprecated). Individual statements are not actually asserted, but an extra triple is added those that are deemed true. For example, the painting “Madonna with the Blue Diadem” (Q738038) has been attributed to Raphael (non asserted statement, ranked as normal) and Gianfrancesco Penni (asserted statement, ranked as preferred and additionally asserted). 

### Ranked statements with qualifiers
- Deprecated ranked statements which have been annotated with "reason for deprecation" (pq:P2241) qualifier. This parameter can tell us why the community decree that an information is not accepted anymore.
- Preferred ranked statements which have been annotated with "reason for " (pq:P7452). This parameter can tell us why the community decree that an information is better than the others. 

## Statements with an uncertain qualifier 
Statements, independently of rank, can be decorated with an additional triple using a specific predicate in the role of qualifier, to annotate its contextual information. We selected those annotated terms which mark uncertainty or debate (e.g. debated, hypothesis, possibly).

- **“Nature of statements” qualifiers**. Predicate pq:P5102 marks the nature of a statement. For example, the painting “Abstract Speed + Sound” (Q19882431) by Giacomo Balla is deemed to be possibly part of a triptych.  
- **"Sourcing circumstances" qualifiers**. As in the previous case, statements can be annotated with a sourcing circumstance (pq:P1480).

## Null-valued objects
A statement can be associated with a blank node. This is meant to imply that the statement is associated with an unknown value, rather than a missing statement. For example, “Missal for the use of the ecclesiastics of Clermont' (Q113302686), an illuminated manuscript from the 14th century, has been recorded with both an unknown creator and author.
