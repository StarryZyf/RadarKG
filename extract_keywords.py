import extract_keywords as ek
import filter_text as ft
import spacy

def process_txt_files(txt_files):
    all_keywords = ek.load_keywords_from_file()
    
    for txt_file in txt_files:
        txt_text = ek.extract_text_from_txt(txt_file)
        rake_keywords = ek.extract_keywords_rake(txt_text)
        tfidf_keywords = ek.extract_keywords_tfidf(txt_text)
        new_keywords = ek.combine_keywords(rake_keywords, tfidf_keywords)
        all_keywords = all_keywords.union(new_keywords)
        
        # 过滤文本
        filtered_text = ft.filter_relevant_sentences(txt_text, all_keywords)
        print(f"Filtered text from {txt_file}:\n{filtered_text}\n")
        
        # 命名实体识别
        nlp = spacy.load("zh_core_web_sm")
        doc = nlp(filtered_text)
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        print(f"Entities in {txt_file}:\n{entities}\n")
        
        # 关系抽取
        relations = extract_relations(doc)
        print(f"Relations in {txt_file}:\n{relations}\n")
    
    ek.save_keywords_to_file(all_keywords)

def extract_relations(doc):
    relations = []
    for sent in doc.sents:
        for ent1 in sent.ents:
            for ent2 in sent.ents:
                if ent1 != ent2:
                    relations.append((ent1.text, "related_to", ent2.text))
    return relations

if __name__ == '__main__':
    txt_files = ["file1.txt", "file2.txt", "file3.txt"]
    process_txt_files(txt_files)

    # 处理新txt文件
    new_txt_text = ek.extract_text_from_txt("new_file.txt")
    keywords = ft.load_keywords_from_file()
    filtered_text = ft.filter_relevant_sentences(new_txt_text, keywords)
    nlp = spacy.load("zh_core_web_sm")
    doc = nlp(filtered_text)
    extracted_info = [(ent.text, ent.label_) for ent in doc.ents]
    relations = extract_relations(doc)
    print(f"Extracted Information from new_file.txt:\n{extracted_info}")
    print(f"Relations from new_file.txt:\n{relations}")
