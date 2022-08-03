#!/usr/bin/env python3 

from neo4j import GraphDatabase

class ConnectGraphDatabase:
    def __init__(self, uri, user, password):
        self.driver = None
        try:
            self.driver = GraphDatabase.driver(uri, auth=(user, password), encrypted=True, trust='TRUST_ALL_CERTIFICATES')
        except Exception as e:
            print("Could not create the driver", e)
        
    def close(self):
        if self.driver is not None:
            self.driver.close()
        
    def query(self, query, db=None):
        assert self.driver is not None, "The driver was not fully initialized"
        session = None
        response = None
        try: 
            session = self.driver.session(database=db) if db is not None else self.driver.session() 
            response = list(session.run(query))
        except Exception as e:
            print("The query did not complete:", e)
        finally: 
            if session is not None:
                session.close()
        return response

def main():
    uri = "neo4j://34.171.95.111:7687"
    user = "neo4j"
    password = "GeneData"

    connection = ConnectGraphDatabase(uri, user, password)

    constraint_query= "CREATE CONSTRAINT FOR (g:Gene) REQUIRE g.Symbol IS UNIQUE;"

    db_query= "USING PERIODIC COMMIT \
        LOAD CSV WITH HEADERS \
        FROM \'https://storage.cloud.google.com/gene_data_csv_files/edges_test.csv\' AS row \
        MERGE (subject:Gene {Symbol: row.subject_symbol}) \
        SET subject.ID = row.subject_id, \
            subject.Prefixes = row.subject_id_prefixes, \
            subject.Category = row.subject_category \
        MERGE (object:Gene {Symbol: row.object_symbol}) \
        SET object.ID = row.object_id, \
            object.Prefixes = row.object_id_prefixes, \
            object.Category = row.object_category \
        CREATE (subject)-[p:PHYSICALLY_INTERACTS_WITH]->(object) \
        SET p.Publications = row.ASSOCIATION_Publications \
        ;"
    
    connection.query(constraint_query, db='neo4j')
    connection.query(db_query, db='neo4j')

if __name__ == "__main__":
    main()