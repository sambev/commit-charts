from time import strptime

# open the raw git log file
logfile = open('../rawgitlog.txt')

all_data = []   # this will hold all the data (commit, author, date)
total_commits = 0       
# this will hold general date data
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
        
        all_data.append(commit_data)

logfile.close()
#print all_data
print date_data
