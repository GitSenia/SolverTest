from requests import Session
from bs4 import BeautifulSoup
from config import config as c

data={'username':c.name,"password":c.password}

work=Session()
work.post(c.url_login,data=data,allow_redirects=True)

for i in range(2):

        respons=work.get(f'{c.url_test}&page={i}')
        soup=BeautifulSoup(respons.text,'lxml')
        #answer=type_of_batton(soup)

        q=soup.find_all("div", class_="flex-fill")
        a=[]
        for j in q:
                a.append(j.text)
        print(a)




