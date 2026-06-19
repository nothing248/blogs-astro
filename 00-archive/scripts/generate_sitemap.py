import markdown
from bs4 import BeautifulSoup
from datetime import datetime
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom
import re


page_regex = r"(.*).md$"
hostname = "https://blogs.service.sxyxy.top"
urlset = Element("urlset")
urlset.attrib["xmlns"] = "http://www.sitemaps.org/schemas/sitemap/0.9"

# 读取文件
with open("../_sidebar.md",'r',encoding='utf-8') as f:
    readme = f.read()
    html = markdown.markdown(readme)
    soup = BeautifulSoup(html,'html.parser')

    links = soup.find_all('a')
    for link in links:
        reg_result = re.match(page_regex,link['href'])
        if reg_result:
            url = SubElement(urlset, "url")
            print(reg_result.group(1))
            SubElement(url, "loc").text = f"{hostname}{reg_result.group(1)}"
            #SubElement(url, "lastmod").text = link['title']
            #SubElement(url, "changefreq").text = ""
            #SubElement(url, "priority").text = ""


# 存储文件
xml_string = minidom.parseString(tostring(urlset)).toprettyxml(indent="  ")
with open("../sitemap.xml", "w", encoding="utf-8") as f:
    f.write(xml_string)
