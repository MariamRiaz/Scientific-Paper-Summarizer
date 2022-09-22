import pandas as pd
import os
import requests

dataframe= pd.read_csv("C:\Users\mariam.riaz\PycharmProjects\Scientific-Paper-Summarizer\Data\talksumm_papers_titles_url.txt", sep = r"\t+", header = None)
output_directory = "C:\Users\mariam.riaz\PycharmProjects\Scientific-Paper-Summarizer\Data\fullpapers"

def url_response_pdf(url):
    name,url = url
    name = str(name)
    if not os.path.isfile(os.path.join(output_directory, name + ".pdf")):
    try:
        response = requests.get(url,stream =True)
        with open(os.path.join(output_directory , name + ".pdf"), "wb") as f:
                for content in r:
                    f.write(content)
        except requests.ConnectionError as e:
            print("Failed to open: " + url)
    

if __name__ == "__main__":
    for rows in dataframe.iterrows():
        url_response(rows[1])