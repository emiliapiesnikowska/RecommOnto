# RecommOnto – Contextual Recommendation Ontology

**RecommOnto** is a contextual ontology for recommendation systems, developed using **Protégé**. It integrates data from multiple domains (movies, books, music) and supports semantic querying through **SPARQL**. The project includes the ontology, linked datasets in RDF format, and a set of pre-defined queries with results.

## Getting Started

### 1. Open the ontology in Protégé

1. Clone this repository or download it as a ZIP.
2. Launch **[Protégé](https://protege.stanford.edu/)**.
3. Open the ontology file
RecommOnto/recommandations.ttl (it is compressed to recommandations.zip file)


### 2. Import datasets (if not loaded automatically)

If the individuals or data instances are not visible, import them manually in Protégé:

- Go to `File > Import...`
- Select format `RDF/XML` or `Turtle`, and import the following files:

DataUploader/output_LDOS-comoda.ttl
DataUploader/amazon_books.ttl (this file is also compressed to .zip, so it needs to be unpacked first)
DataUploader/pitchfork_album_reviews.ttl

- After importing, it’s recommended to **reopen the ontology**, by rebooting protege tool to ensure all data is correctly displayed.

### 3. Explore the ontology

Using Protégé, you can:

- Browse **classes**, **individuals**, and **object/data properties**
- Analyze class hierarchies and semantic relationships

## SPARQL Queries & GraphDB

To run SPARQL queries on the ontology, the project uses **[GraphDB](https://www.ontotext.com/products/graphdb/)**.

### Running queries in GraphDB

1. Install GraphDB or run the desktop version.
2a. Upload repository setup from GraphDBRepository/RecommOnto-config.ttl  
  - In this repository, the queries with output should be visible and exploring output data is available
If anything goes wrong with uploading ready repository:
2b. Create a new repository and upload the following files:
 - `recommandations.ttl`
 - All `.ttl` data files from the `DataUploader/` directory



### Query results

- SPARQL query results used in the related publication are stored in:
    /QueryResults
  - Results are saved as `.csv` files.
## Requirements

- [Protégé](https://protege.stanford.edu/) (version 5.5 or later recommended)
- [GraphDB](https://www.ontotext.com/products/graphdb/) (Community or Free edition)
- RDF data format (Turtle `.ttl` and OWL)




