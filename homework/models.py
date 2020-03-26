okapi_tf = 'result/okapi_tf.txt'
query = "who killed jenna"


stop_words = []

def extraxtQueryFields(query_raw):
    (query_number, query_value) = query_raw.split(maxsplit=1)
    return (query_number, query_value)

with open("stop-list.txt", "r") as f:
    stop_words = f.readlines()
stop_words= [x.strip() for x in stop_words] 
    

with open("queries.txt", "r") as file:
    for line in file:
        if line != "\n" and line != "":
             query_raw = line.replace('\n', '').lower()
             (query_number, query_value) = extraxtQueryFields(query_raw)

class models:
    def __init__(self):
        self.average_doc_length = 5  
        self.merged_catalog = self.store_merged_catalog()  
    
    def store_merged_catalog(self):
        return {'hello':(0,155), 'kevin': (155, 453), 'john': (453, 1999), 'micke': (1999, 10000)}
        
    def get_documents_with_matching_words(self, query):
        dic_docs = {}
        for word in query.split():
            ## steep 1: search if the given word is present in the catalog (as key). If present, read it's corresponding value on the merged index. 
            if word in self.merged_catalog.keys():
                print(self.merged_catalog[word])
        
            
            
    def get_document_length(self, document_dictionary):
        count = 0
        for item in document_dictionary.values():
            count = count + len(item)
        return count
    
    def get_vocablary_length(self, document_dictionary):
        size_document = len(document_dictionary.values())
        return size_document
    
    
    def write_results(self, query_number, model, is_stemmed, dic_results):
        folder = "results/" + is_stemmed + "/" + model + "/"
        with open(folder + query_number + ".txt", "w") as results:
            current_rank = 1
            for item in dic_results:
                results.write("rank " + str(current_rank) + " - " + item[0] + " - score: " + str(item[1]) + "\n")
                current_rank = current_rank + 1
                if(current_rank > 1000):
                    break
    
    def okapi_tf(self, query):
        ##dic_docs = get_documents_with_that_word(query)
        dic_docs = {
            'doc_1': {'dog': [3,19,89], 'eat': [12, 45, 84, 484, 93, 384, 99, 3, 37]},
            'doc_2': {'pizza': [10, 12], 'delivery': [1], 'student': [6]},
            'doc_3': {'ursua': [3]},
            'doc_4': {'eat': [3, 12], 'miam': [120], 'dog': [55]},
            'doc_5': {'shit': [3, 12]},
            }
        
        results = {}
        for document in dic_docs:
            doc_length = self.get_document_length(dic_docs[document])
            okapi_tf_score = 0
            for term in query.split():
                term_okapi_tf = 0
                if term in dic_docs[document].keys():
                    tf = len(dic_docs[document][term]) / doc_length
                    term_okapi_tf = tf / (tf + 0.5 + 1.5 * (doc_length / self.average_doc_length))
            okapi_tf_score += term_okapi_tf
            results[document] = okapi_tf_score
        sorted_dictionnary = sorted(results.items(), key=lambda x: x[1], reverse=True)
        self.write_results(query, "okapi_tf" ,"not_stemmed" , sorted_dictionnary)
        
        

modelOne = models()
modelOne.okapi_tf("the world is dog")