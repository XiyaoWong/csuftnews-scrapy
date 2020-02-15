import re


def clean_html(text: str) -> str:  # 清除不必要的标签属性
    p = re.compile(r'\b(?!(?:href|src|color))\w+=(["\']).+?\1', re.I)
    return p.sub('', text)


def clean_date(date: str) -> int:  # 转换成20200202形式的数字
    return int(date
                .replace("-", "")
                .replace("：", "")
                .replace("来源", '')
                .replace("编辑", '')
                .replace("次浏览", '')
                .strip())

if __name__ == "__main__":
    a = clean_date('2020-02-11\u3000来源：\u3000编辑：\u3000')
    print(a)