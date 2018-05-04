import os
import csv


with open("/Users/encore1125/Desktop/email.csv", "wb") as out_file:
    fieldnames = ['Date', 'From','To','Cc','Bcc','Subject']
    writer = csv.DictWriter(out_file, fieldnames=fieldnames)
    writer.writeheader()
    for root, dirs, files in os.walk("/Users/encore1125/Downloads/enron_with_categories", topdown=False):
        for name in files:
            filePath = os.path.join(root, name)
            if (filePath.endswith(".txt")):
                #if i >3:
                #    continue
                f = open(filePath,"r")
                content = f.read()
                separator = content.find("\r\n\r\n",1)#split("\r\n\r\n")
                emailInfo = content[0:separator]
                emailDate = emailInfo[emailInfo.find("Date:",1):emailInfo.find("From:",1)].strip("\r\n")[5:]
                emailFrom = emailInfo[emailInfo.find("From:",1):emailInfo.find("To:",1)].strip("\r\n")[5:]
                emailTo = emailInfo[emailInfo.find("To:",1):emailInfo.find("Subject:",1)].replace("\r\n","").strip("\r\n")[4:]
                emailCc = ""
                emailBcc = emailInfo[emailInfo.find("Bcc:",1):emailInfo.find("X-From:",1)].replace("\r\n","")[4:]
                sub = content[0:emailInfo.find("Mime-Version:",1)].strip("\r\n")
                cc =  sub.find("Cc:",1)
                #print cc
                if cc!=-1:
                    emailSubject = emailInfo[sub.find("Subject:",1):cc].strip("\r\n")[8:]
                    emailCc = emailInfo[emailInfo.find("Cc:",1):emailInfo.find("Mime-Version:",1)].replace("\r\n","").strip("\r\n")[3:]
                else:
                    emailSubject = content[sub.find("Subject:",1):emailInfo.find("Mime-Version:",1)].strip("\r\n")[8:]

                #print [emailDate,emailFrom,emailTo,emailSubject,emailCc,emailBcc]
                #toemails = emailTo


                writer.writerow({"Date":emailDate,"From":emailFrom,"To":emailTo.replace("\r\n","")\
                    ,"Subject":emailSubject, "Cc":emailCc,"Bcc":emailBcc})

                #print content[separator:]
                f.close()
