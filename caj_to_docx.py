import os
from pycaj2pdf import caj2pdf

def caj_to_pdf(caj_file_path, pdf_file_path):
    """
    将CAJ文件转换为PDF文件
    :param caj_file_path: CAJ文件路径
    :param pdf_file_path: 输出PDF文件路径
    """
    caj2pdf(caj_file_path, pdf_file_path)
    print(f"CAJ文件 {caj_file_path} 已成功转换为PDF文件 {pdf_file_path}")

def main():
    # 示例CAJ文件路径和输出PDF文件路径
    caj_file_path = 'example.caj'
    pdf_file_path = 'example.pdf'
    
    # 调用caj_to_pdf函数进行转换
    caj_to_pdf(caj_file_path, pdf_file_path)

if __name__ == "__main__":
    main()

'''
高校技术转移 复杂网络 科技中介
本研究研究中关村高校技术转移网络，运用复杂网络研究区域特性，解决技术转移难题，提高科技园的技术转移效率。研究发现：(1)中关村技术转移网络合作较为紧密，高价值专利伴随着紧密的合作往来；(2)中关村技术转移网络呈现“小世界”特征；(3)上述网络中北航在各中心性评估中均居于最中心的位置；北京路浩知识产权代理有限公司和高航律师事务所是中关村科技中介中作用最显著的两家企业，对于科技中介发展有借鉴作用。

本文从微观层面研究中关村高校技术转移网络，搜集并分析了四所转化成果最多的高校数据，分别是清华大学、北京大学、北京航空航天大学、中国农业大学2020到2025年的专利转化数据，描绘网络特征，分析突出问题。本文的创新点主要在于将社交网络研究运用于高校和科技中介网络与关系研究，并且从足够微观的角度出发，解读中关村发展现状，得出足够具有现实参考意义的结论。

过往的研究缺乏对于微观层面的实证研究，本研究弥补了这一点；同时较少有研究将复杂网络运用于高校技术转移关系层面加以剖析技术转移问题，本研究结合了复杂网络对症提出改进方案。
'''