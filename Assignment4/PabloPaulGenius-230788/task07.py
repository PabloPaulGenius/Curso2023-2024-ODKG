# -*- coding: utf-8 -*-
"""Task07.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1xuF0danJOpZLpwcyK4JeVcEUQxaqcXgr

**Task 07: Querying RDF(s)**
"""

!pip install rdflib
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2023-2024/master/Assignment4/course_materials"

"""First let's read the RDF file"""

from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage+"/rdf/example6.rdf", format="xml")

"""**TASK 7.1: List all subclasses of "LivingThing" with RDFLib and SPARQL**"""

# TO DO
# Visualize the results

#for r in g.query(q1):
#  print(r)
g.parse(github_storage+"/rdf/example6.rdf", format="xml")

# Define namespaces
rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")

# Define a SPARQL query to find subclasses of "LivingThing"
query = prepareQuery("""
    SELECT ?subclass
    WHERE {
        ?subclass rdfs:subClassOf* <http://example.org/LivingThing>
    }
""")

# Execute the query and print the results
for row in g.query(query):
    print(row.subclass)

"""**TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**

"""

from rdflib.plugins.sparql import prepareQuery
rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")

# Define a SPARQL query to find individuals of "Person" and its subclasses
query = prepareQuery("""
    SELECT ?individual
    WHERE {
        ?individual rdf:type/rdfs:subClassOf* <http://example.org/Person>
    }
""")

# Execute the query and print the results
for row in g.query(query):
    print(row.individual)

"""**TASK 7.3: List all individuals of "Person" or "Animal" and all their properties including their class with RDFLib and SPARQL. You do not need to list the individuals of the subclasses of person**

"""

query = prepareQuery("""
    SELECT ?individual ?property ?value ?class
    WHERE {
        ?individual rdf:type ?class.
        FILTER (?class = <http://example.org/Person> || ?class = <http://example.org/Animal>)
        ?individual ?property ?value.
    }
""")

# Execute the query and print the results
for row in g.query(query):
    print("Individual:", row.individual)
    print("Property:", row.property)
    print("Value:", row.value)
    print("Type:", row.type)
    print()

"""**TASK 7.4:  List the name of the persons who know Rocky**"""

foaf = Namespace("http://xmlns.com/foaf/0.1/")

# Define a SPARQL query to find persons who know "Rocky"
query = prepareQuery("""
    SELECT ?personName
    WHERE {
        ?person foaf:knows ?rocky.
        ?person foaf:name ?personName.
        ?rocky foaf:name "Rocky".
    }
""", initNs={"foaf": foaf})

# Execute the query and print the names of persons who know "Rocky"
for row in g.query(query):
    print(row.personName)

"""**Task 7.5: List the entities who know at least two other entities in the graph**"""

query = prepareQuery("""
    SELECT ?entity
    WHERE {
        ?entity foaf:knows ?person1.
        ?entity foaf:knows ?person2.
        FILTER (?person1 != ?person2)
    }
""", initNs={"foaf": foaf})

# Execute the query and print the entities who meet the criteria
known_entities = set()  # To store the entities that meet the criteria
for row in g.query(query):
    known_entities.add(row.entity)

# List the entities who know at least two others
for entity in known_entities:
    print(entity)