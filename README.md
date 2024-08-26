# RadarKG

## install
pip install pymupdf pytesseract pillow  

sudo apt-get update  
sudo apt-get install tesseract-ocr  
sudo apt-get install tesseract-ocr-chi-sim  

pip install spacy  
python -m spacy download zh_core_web_sm  

pip install rake-nltk scikit-learn

pip install py2neo
export HF_ENDPOINT=https://hf-mirror.com


pip install pygraphviz
sudo apt-get install graphviz


## run
python OCR.py # pdf2txt
python download.py # 安装库
python clear_neo4j.py # 清除知识图谱中全部内容
python QAA.py # 提取关键词、实体、实体关系，构建知识图谱并图形化表示
    需要更改文件存放路径及neo4j用户名和密码