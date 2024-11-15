import re
import pdfplumber
import os

alphabets= "([A-Za-z])"
prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = "(Mr|Mrs|Ms|Dr|Prof|Capt|Cpt|Lt|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = "[.](com|net|org|io|gov|edu|me)"
digits = "([0-9])"
multiple_dots = r'\.{2,}'

def split_into_sentences(text: str) -> list[str]:
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


def pdf_to_clean_text(pdf_path):
    # PDF转文本
    raw_text = pdf_to_text(pdf_path)
    # 清洗文本
    cleaned_text = clean_text(raw_text)
    # 分段处理
    chunks = split_into_sentences(cleaned_text)

    return chunks





