# RecommOnto – Contextual Recommendation Ontology

**RecommOnto** is a contextual ontology for recommendation systems, developed using **Protégé**. It integrates data from multiple domains (movies, books, music) and supports semantic querying through **SPARQL**. The project includes the ontology, linked datasets in RDF format, and a set of pre-defined queries with results.

## Getting Started

### 1. Open the ontology in Protégé
Version of Protégé that was used in project was Protégé 5.6.5.0
1. Clone this repository or download it as a ZIP.
2. Launch **[Protégé](https://protege.stanford.edu/)**.
3. Open the ontology file
RecommOnto/recommandations.ttl (it is compressed to recommandations.zip file)


### 2. Import datasets (if not loaded automatically)

If the individuals or data instances are not visible, import them manually in Protégé:

- Go to `Active ontology` tab, then `Ontology imports` and choose plus icon near to 'Direct imports'
  ![image](https://github.com/user-attachments/assets/f2d0f0cf-48a8-4c5a-84f1-8e9decd596f5)

- Select format `RDF/XML` or `Turtle`, and import the following files:

DataUploader/output_LDOS-comoda.ttl
DataUploader/amazon_books.ttl (this file is also compressed to .zip, so it needs to be unpacked first)
DataUploader/pitchfork_album_reviews.ttl

- After importing, it’s recommended to **reopen the ontology**, by rebooting protege tool to ensure all data is correctly displayed.

In case of issues with missing import:
![image](https://github.com/user-attachments/assets/7da4a568-1da7-471e-af13-01ed4132a30d)

User should choose option 'Yes' and add missing .ttl file that name matches filename from /DataUploader folder.

### 3. Explore the ontology

Using Protégé, you can:

- Browse **classes**, **individuals**, and **object/data properties**
- Analyze class hierarchies and semantic relationships

To explore individual entities go to `Entities` tab -> `Individuals`
![image](https://github.com/user-attachments/assets/67dfff2f-af8e-4f76-b90a-bc0b0beb3fc1)

To explore hierarchy of ontology go to  `Entities` tab -> `Classes`
Set View settings to "Show only the active ontology" to explore RecommontoHierarchy and hide classes from imported ontologies that were not yet used.
![image](https://github.com/user-attachments/assets/bc5e3dc1-81b9-4357-bffb-238ebb3ef450)


## SPARQL Queries & GraphDB

To run SPARQL queries on the ontology, the project uses **[GraphDB](https://www.ontotext.com/products/graphdb/)**. Version that was used in project is: GraphDB 11.0.

### Running queries in GraphDB

1. Install GraphDB or run the desktop version.
2. Create a new repository and upload the following files:
 - RecommOnto/recommandations.ttl (it is compressed to recommandations.zip file) 
 - All `.ttl` data files from the `DataUploader/` directory (amazon_books.ttl is also in .zip file)
   ![image](https://github.com/user-attachments/assets/952ef434-6fc3-47fa-a545-9c8555d9331a)
   ![image](https://github.com/user-attachments/assets/4847b0ce-ba79-412c-bdd9-b54f81d91b41)


3. After succesfully uploading '.ttl' files, it is possible to explore queries result in SPARQL tab.
   - Sample queries are kept in repository in folder RecommOnto/SarqlQueries
4. After running the Queries, it will be possible to explore the results
   ![image](https://github.com/user-attachments/assets/25d76e94-d2a7-4fb9-8298-076a7cc07cd2)
5. Results can be download in several formats:
   
   ![image](https://github.com/user-attachments/assets/8524dc4f-125f-492c-92cd-fd3bd5117346)


### Query results

- SPARQL query results used in the related publication are stored in:
    /QueryResults
  - Results are saved as `.csv` files.
## Requirements

- [Protégé](https://protege.stanford.edu/) (version 5.5 or later recommended)
- [GraphDB](https://www.ontotext.com/products/graphdb/) (Community or Free edition)
- RDF data format (Turtle `.ttl` and OWL)




