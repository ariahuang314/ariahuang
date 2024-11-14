import os
import re
import pdfplumber

def split_into_sentences(text: str) -> list[str]:
    alphabets= "([A-Za-z])"
    prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
    suffixes = "(Inc|Ltd|Jr|Sr|Co)"
    starters = "(Mr|Mrs|Ms|Dr|Prof|Capt|Cpt|Lt|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
    acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
    websites = "[.](com|net|org|io|gov|edu|me)"
    digits = "([0-9])"
    multiple_dots = r'\.{2,}'


    """
    Split the text into sentences.

    If the text contains substrings "<prd>" or "<stop>", they would lead 
    to incorrect splitting because they are used as markers for splitting.

    :param text: text to be split into sentences
    :type text: str

    :return: list of sentences
    :rtype: list[str]
    """
    text = " " + text + "  "
    text = text.replace("\n"," ")
    text = re.sub(prefixes,"\\1<prd>",text)
    text = re.sub(websites,"<prd>\\1",text)
    text = re.sub(digits + "[.]" + digits,"\\1<prd>\\2",text)
    text = re.sub(multiple_dots, lambda match: "<prd>" * len(match.group(0)) + "<stop>", text)
    if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
    text = re.sub("\s" + alphabets + "[.] "," \\1<prd> ",text)
    text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>",text)
    text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
    text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
    text = re.sub(" " + alphabets + "[.]"," \\1<prd>",text)
    if "”" in text: text = text.replace(".”","”.")
    if "\"" in text: text = text.replace(".\"","\".")
    if "!" in text: text = text.replace("!\"","\"!")
    if "?" in text: text = text.replace("?\"","\"?")
    text = text.replace(".",".<stop>")
    text = text.replace("?","?<stop>")
    text = text.replace("!","!<stop>")
    text = text.replace("<prd>",".")
    sentences = text.split("<stop>")
    sentences = [s.strip() for s in sentences]
    if sentences and not sentences[-1]: sentences = sentences[:-1]
    return sentences

def pdf_to_text(file_path):
    # 使用pdfplumber打开PDF文件
    with pdfplumber.open(file_path) as pdf:
        # 初始化一个空字符串来保存文本内容
        text = ""

        # 遍历PDF中的每一页
        for page in pdf.pages:
            # 提取页面的文本并添加到text变量中
            text += page.extract_text()
            text += "\n\n"  # 添加换行符以分隔不同页面的内容

    return text

def clean_text(text):
    # 移除多余的空格和换行
    text = re.sub(r'\s+', ' ', text)
    # 移除页面编号、页眉页脚等
    text = re.sub(r'Page \d+|\f', '', text)
    # 移除不需要的符号
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)  # 移除非ASCII字符
    # 确保句号、问号、感叹号、分号后有空格，不影响小数
    # text = re.sub(r'(?<=[.?!;])(?=\s*[A-Za-z])', ' ', text)
    return text.strip()

def pdf_to_clean_text(pdf_path, output_txt_path):
    # PDF转文本
    raw_text = pdf_to_text(pdf_path)
    # 清洗文本
    cleaned_text = clean_text(raw_text)
    # 分段处理
    chunks = split_into_sentences(cleaned_text)
    
    # 写入到TXT文件，每段写入一行
    with open(output_txt_path, 'w', encoding='utf-8') as f:
        for chunk in chunks:
            f.write(chunk + '\n')
    
    print(f"Cleaned text saved to {output_txt_path}")

def load_file():
    # 指定文件夹路径
    folder_path = '../upload/' # 可以换upload
    # 获取文件夹中的所有文件路径，并过滤出文件（不包含子文件夹）
    files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    # 获取最新的文件（按修改时间排序）
    latest_file = max(files, key=os.path.getmtime)
    # 获取最新文件的文件名
    latest_file_name = os.path.basename(latest_file)
    # print("The lastest file:", latest_file_name)
    file = folder_path + latest_file_name
    outputfile = '../txt/'+ latest_file_name[:-4]+'.txt'
    pdf_to_clean_text(file, outputfile)
    companyname = latest_file_name.split('_')[0]
    print("Convert to txt successful: ", latest_file_name)\
    
    return latest_file_name[:-4], companyname, outputfile




