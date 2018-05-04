import os
import csv


with open("/Users/encore1125/Desktop/email.csv", "wb") as out_file:
    fieldnames = ['Date', 'From','To','Subject','Content']
    writer = csv.DictWriter(out_file, fieldnames=fieldnames)
    writer.writeheader()
    for root, dirs, files in os.walk("/Users/encore1125/Downloads/enron_with_categories", topdown=False):
        for name in files:
            filePath = os.path.join(root, name)
            if (filePath.endswith(".txt")):

                f = open(filePath,"r")
                content = f.read()
                checkemail = content.find("RE: Eeegads") #search key words
                if checkemail!=-1:
                    print filePath
                f.close()
