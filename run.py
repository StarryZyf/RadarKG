import os
import re
import jieba
import jieba.analyse
from py2neo import Graph
import pygraphviz as pgv

def split_sentences(text):
    sentences = re.split(r'[。！？]', text)
    return [s.strip() for s in sentences if s.strip()]

def parse_txt_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return split_sentences(content)

def extract_keywords(sentences):
    keywords = []
    for sentence in sentences:
        keywords.extend(jieba.analyse.extract_tags(sentence))
    return keywords

def load_keywords_by_category(file_paths):
    categories = {}
    for category, file_path in file_paths.items():
        with open(file_path, 'r', encoding='utf-8') as file:
            categories[category] = [line.strip() for line in file]
    return categories

def parse_paper_directory(directory_path):
    sentences = []
    for filename in os.listdir(directory_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory_path, filename)
            sentences.extend(parse_txt_file(file_path))
    return sentences

def extract_relations(sentences, categories):
    relations = []
    for sentence in sentences:
        entities = jieba.analyse.extract_tags(sentence)
        # 只保留不同类别的实体
        for cat1, entities1 in categories.items():
            for cat2, entities2 in categories.items():
                if cat1 != cat2:
                    for entity1 in entities1:
                        if entity1 in entities:
                            for entity2 in entities2:
                                if entity2 in entities:
                                    relations.append((entity1, entity2))
    return relations

def save_keywords_to_file(keywords, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        for keyword in keywords:
            file.write(f"{keyword}\n")

def connect_to_neo4j(uri, user, password):
    return Graph(uri, auth=(user, password))

def create_nodes_and_relationships_from_relations(graph, relations):
    for entity1, entity2 in relations:
        relationship = "相关"
        graph.run("MERGE (a:Entity {name: $entity1}) "
                  "MERGE (b:Entity {name: $entity2}) "
                  "MERGE (a)-[:RELATION {type: $relationship}]->(b)",
                  entity1=entity1, entity2=entity2, relationship=relationship)

def generate_and_save_knowledge_graph(graph, output_file_path):
    G = pgv.AGraph(directed=True)
    
    query = """
    MATCH (a:Entity)-[r:RELATION]->(b:Entity)
    RETURN a.name, b.name, r.type
    """
    result = graph.run(query).data()
    
    for record in result:
        G.add_edge(record['a.name'], record['b.name'], label=record['r.type'])
    
    G.layout(prog='dot')
    G.draw(output_file_path)

class AnswerSearcher:
    def __init__(self, uri, user, password):
        self.g = Graph(uri, auth=(user, password))
        self.num_limit = 20

    '''执行cypher查询，并返回相应结果'''
    def search_main(self, sqls, keyword):
        final_answers = []
        for sql_ in sqls:
            question_type = sql_['question_type']
            queries = sql_['sql']
            answers = []
            for query in queries:
                ress = self.g.run(query, keyword=keyword).data()  # 传递参数
                answers += ress
            final_answer = self.answer_prettify(question_type, answers)
            if final_answer:
                final_answers.append(final_answer)
        return final_answers

    '''根据对应的question_type，调用相应的回复模板'''
    def answer_prettify(self, question_type, answers):
        final_answer = ''
        if not answers:
            return '很抱歉，我没有找到相关信息。'

        if question_type == 'fault_reason':
            desc = [i['b.name'] for i in answers]
            final_answer = f"雷达故障的原因可能是：{'、'.join(desc[:self.num_limit])}。"
        
        elif question_type == 'model_query':
            desc = [i['a.name'] for i in answers]
            final_answer = f"与雷达型号相关的信息包括：{'、'.join(desc[:self.num_limit])}。"
        
        elif question_type == 'relation_query':
            desc1 = [i['a.name'] for i in answers]
            desc2 = [i['b.name'] for i in answers]
            desc = [f"{a} 与 {b} 之间的关系是 {r['r.type']}" for a, b, r in zip(desc1, desc2, answers)]
            final_answer = f"查询到的关系有：{'；'.join(desc[:self.num_limit])}。"
        
        return final_answer

if __name__ == "__main__":
    # 关键词文件路径，需要按实际情况替换
    keyword_files = {
        "fault_name": "./KnowledgeBase/雷达故障名称.txt",
        "fault_reason": "./KnowledgeBase/雷达故障原因.txt",
        "model_name": "./KnowledgeBase/雷达型号.txt"
    }
    
    categories = load_keywords_by_category(keyword_files)
    
    # 论文文件夹路径，需要按实际情况替换
    paper_folder_path = '../../TXT'
    sentences = parse_paper_directory(paper_folder_path)
    
    relations = extract_relations(sentences, categories)
    
    uri = "bolt://localhost:7687"  # Neo4j数据库的URI
    user = "neo4j"  # Neo4j数据库的用户名
    password = "123456"  # Neo4j数据库的密码，需要按实际情况替换
    graph = connect_to_neo4j(uri, user, password)

    print("正在创建知识图谱......")
    create_nodes_and_relationships_from_relations(graph, relations)
    print("知识图谱创建完成！")
    
    output_graph_path = './knowledge_graph.png'
    print("正在保存知识图谱照片......")
    generate_and_save_knowledge_graph(graph, output_graph_path)
    print(f"知识图谱已保存到 {output_graph_path}")
    
    searcher = AnswerSearcher(uri, user, password)
    