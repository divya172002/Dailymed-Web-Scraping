from bs4 import BeautifulSoup
import os
import pandas as pd
d={'Product':[],'Active Ingredient':[] ,'Basis of Strength':[],'Strength of Active Ingredient':[] ,'Product Type':[],'Item Code':[],'Route of Administration':[],'Active Ingredient/Active Moiety':[]  ,'Inactive Ingredients Name':[],'Strength of Inactive Ingredient':[]
   }

for file in os.listdir("data"):
    try:
        with open(f"data/{file}", encoding="utf-8") as f:
            html_doc=f.read()
        soup = BeautifulSoup(html_doc,'html.parser')

        #product name extraction
        td = soup.find("td", class_="contentTableTitle")
        strong2 = td.find("strong")
        
        Product=strong2.get_text(strip=True)
        
        #  Active Ingredient column extraction
        active_table = None
        for tbl in soup.find_all("table"):
            # check if this table has a header with that text
            header = tbl.find("td", class_="formHeadingTitle")
            if header and "Active Ingredient/Active Moiety" in header.get_text():
                active_table = tbl
                break


        if active_table is not None:
            # find the row(s) containing data (skip header rows)
            for row in active_table.find_all("tr"):
                # skip header rows or rows without <td class="formItem">
                cells = row.find_all("td", class_="formItem")
                if not cells:
                    continue
                # first cell has ingredient name — possibly with <strong>
                name_td = cells[0]
                strong = name_td.find("strong")
                active_ingredient = strong.get_text(strip=True) if strong else name_td.get_text(strip=True)
                
                # whole active ingredient name
                
                act_ing_full = name_td.get_text(strip=True)



                # other columns — basis, strength (if available)
                basis = cells[1].get_text(strip=True) if len(cells) > 1 else ""
                strength_val = cells[2].get_text(strip=True) if len(cells) > 2 else ""
            
        prod_table = None
        for tbl in soup.find_all("table", class_="formTablePetite"):
            header = tbl.find("td", class_="formHeadingTitle")
            if header and "Product Information" in header.get_text():
                prod_table = tbl
                break

        if not prod_table:
            print("No Product Information table found")
        else:
            # set defaults
            product_type = None
            item_code = None
            route = None

            # iterate through rows in that table
            for row in prod_table.find_all("tr"):
                # get all <td> in this row
                tds = row.find_all("td")
                # try to match label → value pairs
                for i in range(len(tds)):
                    td = tds[i]
                    text = td.get_text(strip=True)
                    if text == "Product Type" and i+1 < len(tds):
                        product_type = tds[i+1].get_text(strip=True)
                    elif text.startswith("Item Code"):
                        # the next <td class="formItem"> should have the value
                        if i+1 < len(tds):
                            item_code = tds[i+1].get_text(strip=True)
                    elif text == "Route of Administration" and i+1 < len(tds):
                        route = tds[i+1].get_text(strip=True)

           
            # Find the right table
            inactive_table = None
            for tbl in soup.find_all("table", class_="formTablePetite"):
                header = tbl.find("td", class_="formHeadingTitle")
                if header and "Inactive Ingredients" in header.get_text():
                    inactive_table = tbl
                    break
            inactive_ingredients=[]
            if inactive_table:
                
                for row in inactive_table.find_all("tr"):
                    cells = row.find_all("td", class_="formItem")
                    if len(cells) >= 2:
                        # name
                        name = cells[0].get_text(strip=True)
                        # strength
                        strength = cells[1].get_text(strip=True)
                        inactive_ingredients.append((name, strength))

                # Print or process the extracted data
                for name, strength in inactive_ingredients:
       
        
                    d['Product'].append(Product)
                    d['Active Ingredient'].append(active_ingredient)
                    d['Basis of Strength'].append(basis)
                    d['Strength of Active Ingredient'].append(strength_val)
                    d['Product Type'].append(product_type)
                    d['Item Code'].append(item_code)
                    d['Route of Administration'].append(route)
                    d['Active Ingredient/Active Moiety'].append(act_ing_full)
                    d['Inactive Ingredients Name'].append(name)
                    d['Strength of Inactive Ingredient'].append(strength)
       
    
        # break #if not used break it will give title of every product/just for checking one product
    except Exception as e:
        print(e)
# print(soup.prettify()) #it will give hltm list in cmdpmt

df=pd.DataFrame(data=d)
df.to_excel('data.xlsx')

#steps:
# It iterates over a directory called "data" containing HTML files.

# For each HTML file: parses it (with BeautifulSoup), extracts various pieces of data (product name, active & inactive ingredients, strength, product type, item code, route of administration, etc.).

# Accumulates those data items in a dictionary (d) organized by column names.

# Finally converts that dictionary to a pandas DataFrame and writes to an Excel file (data.xlsx).