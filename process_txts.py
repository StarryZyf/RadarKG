import extract_keywords as ek
import filter_text as ft

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
    
    ek.save_keywords_to_file(all_keywords)

if __name__ == '__main__':
    txt_files = ["file1.txt", "file2.txt", "file3.txt"]
    process_txt_files(txt_files)

    # 处理新txt文件
    new_txt_text = ek.extract_text_from_txt("new_file.txt")
    keywords = ft.load_keywords_from_file()
    extracted_info = ft.filter_relevant_sentences(new_txt_text, keywords)
    print(f"Extracted Information from new_file.txt:\n{extracted_info}")
