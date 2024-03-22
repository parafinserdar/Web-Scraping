import requests
from bs4 import BeautifulSoup

def urunKontrolEt(user_agent):
    URL ='https://www.amazon.com.tr/HP-Diz%C3%BCst%C3%BC-Bilgisayar-GeForce-7Z591EA/dp/B0C85K2TP8/ref=sr_1_19?__mk_tr_TR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=2B240Y8B9LPOH&dib=eyJ2IjoiMSJ9.vz99PFy0e3ZHYelKBW0Xc764AG4118Wk6siZXsSSeguM4YwZP4_VZ-3qQeUJJAFMgnk9xozNN5X4vcS_VHvQQ8qNTEn-0epVAw_fAWHgecoFl0VJt4Y_beIl1x6bWexMnsa_lw-yITpwqsAFas3_rC0Wq2UAkSrUNyeNxuZ6crpLq25aQ3Vd9cnUVoQYKHRNS4E8Oc1DRffgBUMVG5H8yrt8f36XttFukFOzLtUPcNIVoEHUbwMJyEU_VaKsmUIU9H7N2x8Vp95eckPyvqdKi5Pjb4SJzFtA1bClnjQ7-nk.8QMqJNwKEw2Yr6T5hkvLllRZxHgeMDlNIqgkSFEXFcU&dib_tag=se&keywords=bilgisayar&qid=1708862178&sprefix=bilgisayar%2Caps%2C153&sr=8-19'
    headers = {"User-Agent": user_agent}
    sayfa = requests.get(URL, headers=headers)
    icerik = BeautifulSoup(sayfa.content,'html.parser')
    urunAdi = icerik.find(id='productTitle').get_text().strip()
    ucret = icerik.find(class_='a-price-whole').get_text().replace('.','')
    yeniUcret = int(ucret[0:5])

    if yeniUcret < 30999:
        print(f"İndirim var koşşş \nUrun Adi : {urunAdi} \nUrun Fiyati : {yeniUcret} TL \n")
    else:
        print(f"Urun Adi : {urunAdi} \nUrun Fiyati : {yeniUcret} \n")

while True:
    user_agent = input("Lütfen user agent bilginizi giriniz -> (Google search engine'e my user agent yazıp çıkan bilgiyi buraya atın.): ")
    urunKontrolEt(user_agent)
