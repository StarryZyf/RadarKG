import spacy

def filter_relevant_sentences(text, keywords):
    sentences = text.split('。')
    relevant_sentences = [sentence for sentence in sentences if any(keyword in sentence for keyword in keywords)]
    return '。'.join(relevant_sentences)

pdf_text = "./TXT/manual.txt"
keywords = ["雷达", "故障", "信号丢失", "电源故障", "诊断", "问题"]
filtered_text = filter_relevant_sentences(pdf_text, keywords)

nlp = spacy.load("zh_core_web_sm")
doc = nlp(filtered_text)

entities = [(ent.text, ent.label_) for ent in doc.ents]
print(entities)
