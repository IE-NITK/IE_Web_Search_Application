import os
import json

os.chdir("/Users/Abhi/Desktop/IE_Web_Search_Application/wsa_scraper")

f = open('data_trials.json', 'r')
data = json.load(f)
id = 1


f.close()
for i in data['emp_details']:
    data1 = {
        "index": {
            "_id": id
        }
    }
    id += 1
    with open("data_trials_new.json", "a") as f:
        json.dump(data1, f)
        f.write('\n')
        json.dump(i, f)
        f.write('\n')
        # print(data1)
    f.close()
