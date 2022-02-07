import requests
from collections import Counter
from itertools import chain

api_link = "https://ct-mock-tech-assessment.herokuapp.com/"
data_dict = requests.get(api_link).json()

final_invitations = {}
invitations = []
total_countries_list = [] 
us_list = []
ireland_list = []
spain_list = []
mexico_list = []
canada_list = []
singapore_list = []
japan_list = []
uk_list = []
france_list = []

for i in data_dict['partners']:
    if i["country"] == 'United States':
        us_list.append(i)
    elif i["country"] == 'Ireland':
        ireland_list.append(i)
    elif i["country"] == 'Spain':
        spain_list.append(i)
    elif i["country"] == 'Mexico':
        mexico_list.append(i)
    elif i["country"] == 'Canada':
        canada_list.append(i)
    elif i["country"] == 'Singapore':
        singapore_list.append(i)
    elif i["country"] == 'Japan':
        japan_list.append(i)
    elif i["country"] == 'United Kingdom':
        uk_list.append(i)
    elif i["country"] == 'France':
        france_list.append(i)

total_countries_list.append(us_list)
total_countries_list.append(ireland_list)
total_countries_list.append(spain_list)
total_countries_list.append(mexico_list)
total_countries_list.append(canada_list)
total_countries_list.append(singapore_list)
total_countries_list.append(japan_list)
total_countries_list.append(uk_list)
total_countries_list.append(france_list)

def guest_list(a_list):
    country_dict ={}
    total_dates = []
    attendees = []
    country_dict["name"] = (a_list[0]['country'])
    for i in range(len(a_list)):                                    # creates list of all given US dates
        total_dates.append(a_list[i]['availableDates'])
                                      
    flatten_list = list(chain.from_iterable(total_dates))            # flattens list to iterate
    c = Counter(flatten_list)                                        
    common_dates = c.most_common()
    def check_dates():
        check_dates = []
        for d in range(len(common_dates)):
            check_dates.append(int(common_dates[d][0][8:]))         
        flag = True
        while True:                                                         # checks for consecutive dates
            for i in range(len(check_dates)):
                if check_dates[i] - check_dates[i+1] == 1 or check_dates[i] - check_dates[i+1] == -1:
                    flag = False
                    return i
                else:
                    continue
    idx =check_dates()
    
    final_dates = []
    final_dates.append(common_dates[idx][0])
    final_dates.append(common_dates[idx+1][0])                           # creates empty list and adds 2 most common consecutive dates

    for i in range(len(a_list)):
        if set(final_dates).issubset(set(a_list[i]['availableDates'])):    # checks if final dates are in each partners's avail dates
            attendees.append(a_list[i]['email'])                            # if True, returns partner's e-mail                         
    country_dict["startDate"] = (final_dates[0])
    country_dict["attendeeCount"] = len(attendees)                       # adds additional information for each country's meeting
    country_dict['attendees'] = attendees
    return country_dict

def complete_list():                                                       # function adds all country lists to combined list
    for i in total_countries_list:
        invitations.append(guest_list(i))
    return invitations

complete_list()

final_invitations['data'] = invitations                                    # converts all final info to value for key of 'data'
ans = requests.post(url = 'https://ct-mock-tech-assessment.herokuapp.com/', json = {'data':invitations})
print(invitations)
print(ans)