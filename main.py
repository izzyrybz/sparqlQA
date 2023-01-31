
from rdflib import Graph, Literal, Namespace, RDF, XSD, URIRef
import requests

# rdflib knows about quite a few popular namespaces, like W3C ontologies, schema.org etc.

from datetime import datetime
import copy


###################################### TO CREATE THE COMMITS FROM THE TXT ################################################################


#file__name= input("Please provide the file which the history of commits exists:")
path = '/home/bell/commithistory.txt'
commit = {"commit_ref": "", "author": "", "description": "", "date":"" }
history = []
date_format = " %a %b %d %H:%M:%S %Y %z"

def isdictempty(dict):
    for value in dict.values():
        if value:
            return False
        else:
            return True


def info_between_elements(lst, A, B):
    #print(lst)
    result = []
    first_commit_flag = True
    found_A = False
    for i, elem in enumerate(lst):
        #print(elem)
        if A in elem:
            found_A = True
        if found_A:
            elem = elem.strip()
            #print(elem)
            result.append(elem)
        if B in elem:
            if first_commit_flag:
                first_commit_flag=False
                continue
            else:
                break
    result.pop(0)
    result.pop(1)
    #for result
    #print(result)
    return result



with open(path,'r') as f:
    for line in f:
        line = line.strip()
        line = line.split(',')
        if line == ['']:
            continue
        #print(line)
        for index, element in enumerate(line):
            #print(index,element)
            if ('commit' in element and not ('Initial'in element)):
                hash = element[element.index(":") + 1:]
                commit["commit_ref"]  = hash
            if('Author:' in element): 
                #print("adding person",line[index+1])
                name = element[element.index(":") + 1:]
                commit["author"] = name
            if('Description:' in element): 
                #print("adding person",line[index+1])
                description = element[element.index(":") + 1:]
                commit["description"] = description
            if('Date:' in element):
                date = element[element.index(":") + 1:]
                #print("THIS IS DATE:",date)
                date_obj = datetime.strptime(date, date_format)
                #print(date_obj)
                commit["date"] = date_obj
            if('------' in element):
                #print("this is a ",commit)
                history.append(commit)
                commit = copy.deepcopy(commit)
                         
#print(history)


############################################ TO CREATE THE RDF TRIPPLES #############################################

commits = Namespace("http://example.com/commits/")
EX = Namespace("http://example.com/")

data=[]
g = Graph()


'''for commit in history:
    #print(commit["commit_ref"])
    urirefstring = "http://example.org/"+commit["commit_ref"]
    urirefstring= urirefstring.replace(" ", "")
    uriref = URIRef(urirefstring)
    dict = {
        uriref
    }'''
    



for commit in history:
    urirefstring = "http://example.org/"+commit["commit_ref"]
    urirefstring= urirefstring.replace(" ", "")
    commit_uri = URIRef(urirefstring)
    #commit_uri = commits[commit['commit_ref']]
    g.add((commit_uri, RDF.type, EX.Commit))
    g.add((commit_uri, EX.author, Literal(commit['author'])))
    g.add((commit_uri, EX.description, Literal(commit['description'])))
    g.add((commit_uri, EX.date, Literal(commit['date'], datatype=XSD.dateTime)))

# To save the graph to a file
g.serialize(destination='commits.ttl', format='turtle')

################################################## TRYING TO FIGURE OUT HOW TO USE SPARQL ###################################3

query = """
SELECT ?object
WHERE {
	
<http://example.org/65970ecb019eef5a3b2f709180113213e6000a78>
  <http://example.com/author>
   ?object
}
"""

response = requests.get("http://localhost:3030/test4commits/sparql", params={"query": query})
##TODO CHANGE THE http://example.com/sparql with the endpoint of our need.
#print(response)

if response.status_code == 200:
    results = response.json()
    print(results)
    # Process the results
else:
    print("Query failed with status code", response.status_code)

    
    
    
#question =  input("What is your question?")
