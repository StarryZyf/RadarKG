from py2neo import Graph

def clear_neo4j_database(graph):
    query = "MATCH (n) DETACH DELETE n"
    graph.run(query)

# 连接Neo4j数据库
uri = "bolt://localhost:7687"  # Neo4j数据库的URI
user = "neo4j"  # Neo4j数据库的用户名
password = "123456"  # Neo4j数据库的密码
graph = Graph(uri, auth=(user, password))

# 清空数据库
clear_neo4j_database(graph)
print("Neo4j数据库已清空")
