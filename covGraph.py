from sys import argv
from matplotlib import pyplot
import csv
import urllib.request
import codecs

#row:
# index is data
# 0date
# 1dd
# 2mm
# 3yyyy
# 4cases
# 5deaths
# 6countries
# 7geoID
# 8territory code
# 9population data 2019
# 10continent
# 11number for lst 14 days of covid19 per 100 000
def format_data(data):
    maxy = 25
    dates = []
    cases = []
    deaths = []
    cases_per_100K = []
    
    for row in data:
        try:
            case = int(row[4])
            death = int(row[5])
            case_per_100k = float(row[11])
        
            dates.insert(0, row[0])
            cases.insert(0, case)
            deaths.insert(0, death)
            cases_per_100K.insert(0, case_per_100k)
            
            if case > maxy:
                maxy = case
            elif death > maxy:
                maxy = death
        except Exception as e:
            #silently ignore exception
            #print(e)
            pass
        
    return dates, cases, deaths, cases_per_100K, maxy


def plotData(country, dates, cases, deaths, cases_per_100K, maxy):
    legend = ['cases', 'deaths', 'cases per 100k']
    
    pyplot.title(country)
    pyplot.xlabel("Dates")
    
    pyplot.ylim((0, maxy + 10))
    
    pyplot.plot(dates, cases)
    pyplot.plot(dates, deaths)
    pyplot.plot(dates, cases_per_100K)

    pyplot.legend(legend)

    pyplot.show()


if __name__ == '__main__':
    country = argv[1].upper()
    
    primary_dataset = []

    #https://stackoverflow.com/questions/18897029/read-csv-file-from-url-into-python-3-x-csv-error-iterator-should-return-str
    url = "https://opendata.ecdc.europa.eu/covid19/casedistribution/csv"
    stream = codecs.iterdecode(urllib.request.urlopen(url), 'utf-8')
    csv = csv.reader(stream)

    found = False;
    #row column 6 is country
    for row in csv:
        if row[6].upper() == country:
            primary_dataset.append(row)
            found = True
        elif (found): #if we've found it and we're not on the country anymore
            break;
    
    dates, cases, deaths, cases_per_100K, maxy = format_data(primary_dataset)
    plotData(country, dates, cases, deaths, cases_per_100K, maxy)
    
    lastpos = len(dates) - 1;

    print(f"In {country} got cases {cases[lastpos]}, deaths {deaths[lastpos]}, cases per 100k population {cases_per_100K[lastpos]}.")
    print(f"Maximum all-time recorded cases were {maxy}.")
    
