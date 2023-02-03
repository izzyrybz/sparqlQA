import json
import requests, json, re, operator
import sys
from parser.lc_quad import LC_Qaud
import urllib.parse


def prepare_dataset(ds):
    ds.load()
    ds.parse()
    return ds


def ask_query(uri):
    if uri == "<https://www.w3.org/1999/02/22-rdf-syntax-ns#type>":
        return 200, json.loads("{\"boolean\": \"True\"}")
    uri = uri.replace("https://", "http://")
    return query(u'ASK WHERE {{ {} ?u ?x }}'.format(uri))


def query(q):
    q = q.replace("https://", "http://")
    #q = urllib.parse.quote_plus(q)
    print("THIS IS QUERY:",q)
    r = requests.get("http://localhost:3030/test4commits/sparql",  params={"query": q})
    print("past request")
    print(r.status_code)
    return r.status_code, r.json()


def has_answer(t):
    if "results" in t and len(t["results"]["bindings"]) > 0:
        return True
    if "boolean" in t:
        return True
    return False


if __name__ == "__main__":

    #with open('data/LC-QUAD/train-data.json', 'r', encoding='utf-8') as f:
    #    train = json.load(f)

    with open('data/LC-QUAD/test-data.json', 'r', encoding='utf-8') as f:
        text = json.load(f)


    # Load the JSON text into a Python object
    data = text

    #data = train + test
    print('data len: ', len(data))

    #dump everthing in the file

    with open("data/LC-QUAD/data.json", "w") as write_file:
        json.dump(data, write_file)

    #use file to send to the parser
    ds = LC_Qaud(path="./data/LC-QUAD/data.json")
    print(ds)
    tmp = []
    #for ever loop we take a line in data (aka ds) and load and parse it into qapair
    for qapair in prepare_dataset(ds).qapairs:
        print("in for loops")
        raw_row = dict()
        raw_row["id"] = qapair.id.__str__()
        raw_row["question"] = qapair.question.text
        raw_row["sparql_query"] = qapair.sparql.query
        print("THIS IS question" ,qapair.question.text)
        try:
            #we try to fetch the information from the query
            r = query(qapair.sparql.query)
            raw_row["answers"] = r[1]
            print("THIS IS ANSWER" ,r[1])
        except Exception as e:
            raw_row["answers"] = []

        tmp.append(raw_row)

    with open('data/LC-QUAD/linked_answer.json', 'w') as jsonFile:
        json.dump(tmp, jsonFile)

    print('data len: ', len(tmp))
