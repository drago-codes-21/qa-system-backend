import spacy
import wikipediaapi
from elasticsearch import Elasticsearch
from py2neo import Graph

# Load Spacy NLP model and Wikipedia API
import spacy.cli
spacy.cli.download("en_core_web_sm")
nlp = spacy.load('en_core_web_sm')
wiki_api = wikipediaapi.Wikipedia('en')

# Connect to the Neo4j database
graph = Graph("neo4j+s://b036c990.databases.neo4j.io", auth=("neo4j", "N6mLloy2NdCDSGvYh-g-1xZLrUWJnd5SqS457d9Aiwo"))

# Connect to the Elasticsearch server
ELASTIC_PASSWORD = "VzagjeQRmNuYOsNxCa9qvkpb"

# Found in the 'Manage Deployment' page
CLOUD_ID = "deployment-name:dXMtZWFzdDQuZ2Nw..."

# Create the client instance
es = Elasticsearch(
    "https://localhost:9200",
    basic_auth=("elastic", ELASTIC_PASSWORD)
)

# Successful response!
# es = Elasticsearch()

# Define a function to extract entities from a sentence
def extract_entities(sentence):
    doc = nlp(sentence)
    entities = []
    for ent in doc.ents:
        entity = {}
        entity['text'] = ent.text
        entity['label'] = ent.label_
        entities.append(entity)
    return entities

# Define a function to link entities to Wikipedia pages
def link_entities(entities):
    for entity in entities:
        query = "MATCH (e:Entity {name: $name})-[:MENTIONS]->(page:WikipediaPage) RETURN page.title, page.summary"
        results = graph.run(query, name=entity['text']).data()
        if results:
            entity['wiki'] = results[0]['page.summary']
        else:
            annotations = wiki_api.page(entity['text'])
            if annotations.exists():
                entity['wiki'] = annotations.summary
    return entities

# Define a function to retrieve documents using Elasticsearch
def retrieve_documents(question):
    query = {
        "query": {
            "multi_match": {
                "query": question,
                "fields": ["title^3", "text"]
            }
        }
    }
    result = es.search(index="documents", body=query)
    hits = result['hits']['hits']
    documents = []
    for hit in hits:
        documents.append({
            "title": hit['_source']['title'],
            "text": hit['_source']['text'],
            "score": hit['_score']
        })
    return documents

# Define a function to extract answers to a question
def extract_answer(question):
    parts = question.split("; ")
    answers = []
    for part in parts:
        entities = extract_entities(part)
        linked_entities = link_entities(entities)
        documents = retrieve_documents(part)
        for document in documents:
            doc_entities = extract_entities(document['text'])
            doc_linked_entities = link_entities(doc_entities)
            for entity in linked_entities:
                for doc_entity in doc_linked_entities:
                    if entity['text'] == doc_entity['text']:
                        answers.append(document['text'])
        for entity in linked_entities:
            if 'wiki' in entity:
                answers.append(entity['wiki'])
    if not answers:
        return "Sorry, I couldn't find an answer to your question."
    return ". ".join(answers)

# Example multi-part question and answer extraction
question = "Who is the president of the United States; What is the capital of France?"
answer = extract_answer(question)
print(answer)
