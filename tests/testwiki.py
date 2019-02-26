# import pandas as pd
from bs4 import BeautifulSoup
from mediawikiapi import MediaWikiAPI

def wikitable_to_dataframe(table):
    """
    Exports a Wikipedia table parsed by BeautifulSoup. Deals with spanning: 
    multirow and multicolumn should format as expected. 
    """ 
    rows=table.findAll("tr")
    nrows=len(rows)
    ncols=max([len(r.findAll(['th','td'])) for r in rows])

    # preallocate table structure
    # (this is required because we need to move forward in the table
    # structure once we've found a row span)
    data=[]
    for i in range(nrows):
        rowD=[]
        for j in range(ncols):
            rowD.append('')
        data.append(rowD)

    # fill the table with data:
    # move across cells and use span to fill extra cells
    for i,row in enumerate(rows):    
        cells = row.findAll(["td","th"])
        for j,cell in enumerate(cells):        
            cspan=int(cell.get('colspan',1))
            rspan=int(cell.get('rowspan',1))
            l = 0
            for k in range(rspan):
                # Shifts to the first empty cell of this row
                # Avoid replacing previously insterted content
                while data[i+k][j+l]:
                    l+=1
                for m in range(cspan):
                    data[i+k][j+l+m]+=cell.text.strip("\n")

    return data


mediawikiapi = MediaWikiAPI()
test_page = mediawikiapi.page('List of video games notable for negative reception')
# to check page URL:
print(test_page.url)
soup = BeautifulSoup(test_page.html(), 'html.parser')
# tables = soup.findAll("table", { "class" : "wikitable" })
# headings = soup.findAll('h3')
# df_test = wikitable_to_dataframe(tables[0])
# print(df_test)

for headlines in soup.find_all("h3"):
    print(headlines.text.strip()[:headlines.text.strip().find(' (')])


def headings(page):
    mediawikiapi = MediaWikiAPI()
    page = mediawikiapi.page(page)
    soup = BeautifulSoup(page.html(), 'html.parser')
    data = []
    for headlines in soup.find_all("h3"):
        data.append(headlines.text.strip()[:headlines.text.strip().find(' (')])
    return data

print(headings('List of video games notable for negative reception'))