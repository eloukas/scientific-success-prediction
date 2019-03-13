import pandas as pd
import numpy as np
import sys

rows = {}

# change these values!!
year_range = int(sys.argv[2]) # mexri posa xronia tha einai h xronoseira
zeros_threshold = int(sys.argv[3]) # apo posa mhdenika kai katw krataw to paper

def count_elements(citations, year):
    hist = {}

    for key in citations.keys():
        i = citations[key][year]
        hist[i] = hist.get(i, 0) + + 1

    return hist

def clean_up(citations, num_of_zeros):
    
    return {key: citations[key] for key in citations.keys() if citations[key].count(0)<=num_of_zeros}


def prepare_dataframe(year_range):
    citations = {key: [0 for _ in range(0,year_range+1)] for key in rows.keys()}

    for key in rows.keys():
        year_of_paper = rows[key][0]
        ref_id_list = rows[key][1]

        for ref_id in ref_id_list:
            if (ref_id in citations.keys()):
                diff_in_years = year_of_paper - rows[ref_id][0]
                if (diff_in_years >= 0 and diff_in_years <= year_range):
                    citations[ref_id][diff_in_years] += 1
            
    return (citations)


def read_file(name):
    paper_title = None
    authors = None
    year = 0
    venue = None
    index = -1
    abstract = None
    ref_id_list = []

    with open(name, 'r') as fd:
        lines = fd.readlines()
        for line in lines:
            if (line[0] != '\n'):
                line = line.strip('\n')
                if line[0] == '#':
                    if (line[1] == '*'):
                        paper_title = line[2:]
                    elif(line[1] == '@'):
                        authors = line[2:]
                        #authors = seperate_authors(authors, 1)
                    elif(line[1] == 't'):
                        year = int(line[2:])
                    elif(line[1] == 'c'):
                        venue = line[2:]
                    elif('index' in line[1:6]):
                        index = int(line[6:])
                    elif(line[1] == '%'):
                        ref_id = int(line[2:])
                        ref_id_list.append(ref_id)
                    elif(line[1] == '!'):
                        pass
                        abstract = line[2:]
                    else:
                        pass
            else:
                if (index != -1 and year != 0):
                    rows[index] = [year, ref_id_list]

                    paper_title = None
                    authors = None
                    year = 0
                    venue = None
                    index = -1
                    abstract = None
                    ref_id_list = []

read_file(sys.argv[1])
citations = clean_up(prepare_dataframe(year_range),zeros_threshold)

print('Number of papers: ', len(citations.keys()))
for i in range(0, year_range+1):
    print('year_{} has {}\n'.format(i, count_elements(citations, i)))

columns = ['year_'+str(x) for x in range(0, year_range+1)]
df = pd.DataFrame.from_dict(citations, orient='index',
        columns = columns)
df.to_excel('dataset.xlsx')
