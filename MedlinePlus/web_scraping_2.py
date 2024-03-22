import string  #A-Z tüm büyük harfleri getiren ascii_uppercase için 
import requests #http istekleri için
from bs4 import BeautifulSoup #linkin kaynak kodunda istediğimiz elementi (class,id,ul,li) gibi çekmek için
from tqdm import tqdm #terminalde info vermek için
import json #datayı json türünde toplamak için
import click #kazıma işlemini hızlı yapmak için belirli aralıklara bölüp threadler aracılığla aynı anda kazıma işlemi yapmak için


class Scraper:
    def __init__(self) -> None:
        self.base_url = "https://medlineplus.gov/druginfo" #Temel link bunun üzerine belli düzene göre linkleri oluşturacağım.
        self.drug_links = set()

    def get_categories(self): #sayfadaki A-Z tüm kategorileri getiren fonksiyon
        letters = string.ascii_uppercase  #A-Z tüm harfleri büyük harf olarak getirdim.
        result = list(map(lambda letter: self.base_url + "/drug_{}a.html".format(letter), letters)) #linkleri oluşturdum.
        result.append("https://medlineplus.gov/druginfo/drug_00.html") #Bu aykırı değer bunu elle girmek zorunda kaldım.
        return result

    def get_source(self, url): #her link için source kodunu getiren fonksiyon
        r = requests.get(url) #http isteği attım.
        if r.status_code == 200: #başarılı bir şekilde istek atıldıysa  
            return BeautifulSoup(r.content, "lxml") #r.content-> kaynağı getirir 
        return None

    def get_drug_a_links(self, source): #her bir ilaç linkini getiren fonksiyon
        all_drug_li = source.find("ul", attrs={"id": "index"}).find_all("li") #id'si index olan ul içinden li'lerin hepsini getirdim.
        drug_links = list(
            map(lambda drug: self.base_url + drug.find("a").get("href").replace(".", "", 1), all_drug_li)) #her bir li için hrefleri buldum ve onu bir listeye attım.
        return set(drug_links) #unique döndürüyor,aynı eleman birden fazla bulunmuyor.


    def find_all_drug_links(self): #A-Z tüm ilaçların tüm ilaç linklerini getiren fonksiyon
        categories = self.get_categories()
        bar = tqdm(categories, unit=" category link")
        for category_link in bar:
            category_sources = self.get_source(category_link)
            if category_sources:
                self.drug_links = self.drug_links.union(self.get_drug_a_links(category_sources))
        return self.drug_links

    def get_name(self, source):
        try:
            return source.find("h1", attrs={"class": "with-also"}).text
        except Exception:
            return None

    def get_section_info(self, source, id_element):
        try:
            section = source.find("div", {"id": id_element})
            if section:
                title = section.find("h2").text.strip()
                content = section.find("div", {"class": "section-body"}).text.strip()
                return {"title": title, "content": content}
        except Exception as e:
            print(f"Error retrieving section: {e}")
        return None

    def scrape_drugs(self, start=None, end=None):
        if start is None:
            start = 0

        result = []
        links = list(self.find_all_drug_links())
        if end is None:
            end = len(links)
        bar = tqdm(links[start:end], unit=" drug link")
        for link in bar:
            sections = []
            bar.set_description(link)
            drug_source = self.get_source(link)
            name = self.get_name(drug_source)
            why = self.get_section_info(drug_source, "why")
            sections.append(why)
            how = self.get_section_info(drug_source, "how")
            sections.append(how)
            other_uses = self.get_section_info(drug_source, "other_uses")
            sections.append(other_uses)
            result.append({"name": name, "url": link, "sections": sections})
        return result

    def write_as_json(self, data, filename="datas.json"):
        with open(filename, "w", encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    @click.command()
    @click.option("--start", type=int)
    @click.option("--end", type=int)
    @click.option("--filename", default="datas.json", help="Output filename")
    def run(start, end, filename):
        scraper = Scraper()
        data = scraper.scrape_drugs(start, end)
        scraper.write_as_json(data, filename)

    run()

#Örnek kullanım terminalde

#python web_scraping_2.py --start 0 --end 50 --filename p1.json
#python web_scraping_2.py --start 50 --end 100 --filename p2.json
#python web_scraping_2.py --start 100 --end 150 --filename p3.json
#farklı farklı terminaller açıp hızlıca kazıma yapılabilir.