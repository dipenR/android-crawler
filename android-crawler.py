from urllib.request import urlopen as url_open
from bs4 import BeautifulSoup as soup
import os

def returnSoup(url):
    
    htmlReader = url_open(url)
    page_text = htmlReader.read()
    htmlReader.close()
    
    page_soup = soup(page_text, "html.parser")
    
    return page_soup


if __name__ == "__main__":
    url = 'https://developer.android.com/reference/android/app/'
    start_url = url + "package-summary" # 'https://developer.android.com/reference/android/app/package-summary' 
    
    page_soup = returnSoup(start_url)
    
    containers = page_soup.find_all('table', {"class":"jd-sumtable-expando"})

    # FILE STUFF ----
    direc = os.path.join(os.getcwd(), 'outFiles')
    if not os.path.exists(direc):
        os.mkdir(direc)
        
    os.chdir(direc)
    current_dir = os.getcwd()

    all_ice = []
    for item in containers:
        all_ice.append(item.find_all('td', {"class": "jd-linkcol"}))
    
    interfaces, classes, exceptions = all_ice
    all_ice = [] + interfaces + classes + exceptions
    
    ice_urls_names = {}
    for ice in all_ice:
        ice_name = ice.find('a').string
        ice_urls_names[ice_name] = str(url + ice_name)
        
    for ice_name, ice_url in ice_urls_names.items(): # start crawling to all webpages we need to traverse through
        page_soup = returnSoup(ice_url)
        conts = page_soup.find('div', {"id": "jd-content"})
                
        for cont in conts.findAll('p', {"class": ["note", "caution"]}):
            #print(ice_url + "      " + ice_name)
            
            note_text = cont.get_text()
            #print(cont.get_text() +"\n\n\n")
            
            name = cont.parent.parent.find('h3')
            if (name is None):
                continue
            name = name.string
            if ' ' in name:
                continue
            #print("||"+name+"||\n\n")
            
            # now name stores name of method/constant that has the note/caution   name-->m/c name
            # ice_url stores url, ice_name stores name of I/C/E   ice_name--> name of I/C/E
            # note_text stores text of the note at any given url/method    note_text--> text of note
            
            file_name = str(ice_name.split(".")[0]) + ".txt"
            f = open(file_name, "w")
            
            note_text = " ".join(note_text.split())
            string_to_write = name + ":" + note_text
            print(string_to_write)
            f.write(string_to_write)
            
            f.close()
            

            
            
            
            