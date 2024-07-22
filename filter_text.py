import json

def load_keywords_from_file(filename="keywords.json"):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            keywords = json.load(f)
            return set(keywords)
    except FileNotFoundError:
        return set()

def filter_relevant_sentences(text, keywords):
    sentences = text.split('。')
    relevant_sentences = [sentence for sentence in sentences if any(keyword in sentence for keyword in keywords)]
    return '。'.join(relevant_sentences)

if __name__ == '__main__':
    text = "从某个txt文件提取的示例文本。包含雷达和故障的相关信息。"
    keywords = load_keywords_from_file()
    filtered_text = filter_relevant_sentences(text, keywords)
    print(filtered_text)
