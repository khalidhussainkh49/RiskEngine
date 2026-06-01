from neo4j import GraphDatabase
from app.core.config import settings

class GraphService:
    def __init__(self):
        self.driver = GraphDatabase.driver(
            settings.NEO4J_URI,
            auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
        )

    def close(self):
        self.driver.close()

    def map_declaration(self, sgd_id, importer_tin, importer_name, items):
        with self.driver.session() as session:
            session.execute_write(self._create_nodes, sgd_id, importer_tin, importer_name, items)

    @staticmethod
    def _create_nodes(tx, sgd_id, importer_tin, importer_name, items):
        query = """
        MERGE (d:Declaration {sgd_id: $sgd_id})
        MERGE (i:Company {tin: $importer_tin})
        SET i.name = $importer_name
        MERGE (d)-[:HAS_IMPORTER]->(i)
        WITH d
        UNWIND $items AS item
        MERGE (h:HSCode {code: item.hs_code})
        MERGE (d)-[:CONTAINS_HS]->(h)
        """
        tx.run(query, sgd_id=sgd_id, importer_tin=importer_tin, importer_name=importer_name, items=items)
