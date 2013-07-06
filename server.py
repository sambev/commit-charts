from flask import Flask
from config.jconfig import render
import json

from time import strptime

app = Flask(__name__)

@app.route("/")
def index():
    return render('index.html') 


@app.route("/get_json")
def getJSON():
    # open the raw git log file
    logfile = open('rawgitlog.txt')
  
    all_data = {}
    commit_list = []   # this will hold all the data (commit, author, date)
    total_commits = 0       
    date_data = {}

    for line in logfile:
        """
        Sort the data in a json like format:
            {
                'commit': <sha>,
                'author': <author|email>,
                'date': <date>
            }
        """
        if 'commit' in line[:6]:
            commit_data = {}    # this dict is just for each commit, it is appended to all data at the end
            total_commits += 1
            commit_data['commit'] = line[7:].strip(' \t\n\r')

        elif 'Author' in line[:7]:
            commit_data['author'] = line[8:].strip(' \t\n\r')

        elif 'Date' in line[:5]:
            nice_date = line[8:32].strip(' \t\n\r')
            commit_data['date'] = nice_date     # add it to the commit data
            # make a time struct so we can easily find more info about the date
            ts = strptime(nice_date)
            # collect the general date data
            if ts.tm_year not in date_data:
                date_data[ts.tm_year] = {
                    1:0,
                    2:0,
                    3:0,
                    4:0,
                    5:0,
                    6:0,
                    7:0,
                    8:0,
                    9:0,
                    10:0,
                    11:0,
                    12:0
                }
            else:
                date_data[ts.tm_year][ts.tm_mon] += 1
        
        commit_list.append(commit_data)

    logfile.close()
    # get the highest number of commits by month:
    amount_list = []
    for year in date_data:
        for month in date_data[year]:
            amount_list.append(date_data[year][month])
    
    all_data['commit_high'] = max(amount_list)
    all_data['date_data'] = date_data
    all_data['total'] = total_commits

    # return the git log in json form 
    return json.dumps(all_data)


if __name__ == "__main__":
    app.debug = True
    app.run()
