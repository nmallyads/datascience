# coding=utf-8
import pandas as pd
import xml.etree.ElementTree as ET
tree = ET.parse('./data/mondial_database.xml')

root = tree.getroot()

#name and country of a) longest river, b) largest lake and c) airport at highest elevation

#10 ethnic groups with the largest overall populations (sum of best/latest estimates over all countries)
def find_ethnic_groups_with_largest_population(n):
    ethnic_group_dict = {}
    for child in root:

        #for population in child.getiterator('population'):
        population_list = child.findall('population')
        len_pop = len(population_list)
        if(len_pop > 0):
            #get the latest year and it's population
            country_population = (population_list[len_pop - 1].text)

        country_name = child.find('name').text
        # get largest ethnic group
        temp_percent = 0
        for ethnic_group in child.getiterator('ethnicgroup'):
            if ethnic_group is not None:
                ethnic_gp_percent = float(ethnic_group.get('percentage'))
                if( ethnic_gp_percent > temp_percent):
                    ethnic_group_name = ethnic_group.text
                    temp_percent = float(ethnic_group.get('percentage'))
        ethnic_population = (temp_percent * float(country_population))/100
        if(ethnic_population > 0):
            key = country_name + '[' +  ethnic_group_name + ']'
            value = ethnic_population
            ethnic_group_dict[key] = float(value)

    ethnic_group_series = pd.Series(ethnic_group_dict).sort_values(ascending=False)
    print('\nThe ' + str(n) + ' ethnic groups with the largest population')
    print(ethnic_group_series[:n])

#find_ethnic_groups_with_largest_population(10)

# private function to help populate the dictionary containing cities and populations
def update_population_dictionary(country_name, parent_element, year_population_dict):
    for city in parent_element.getiterator('city'):
        if city is not None and city.find('name') is not None:
            # print()
            city_name = city.find('name').text

            country_city = country_name + '_' + city_name
            for population in city.getiterator('population'):
                key = int(population.get('year'))

                if key in year_population_dict:
                    value_dict = year_population_dict[key]
                    value_dict[country_city] = int(population.text)
                else:
                    value_dict = {}
                    value_dict[country_city] = int(population.text)
                    year_population_dict[key] = value_dict


# Find 10 cities with the largest population
def find_n_cities_with_largest_population_for_year(n, year):
    year_population_dict = {}
    for child in root:
        country_name = child.find('name').text

        # for data where the city is a child of country
        update_population_dictionary(country_name, child, year_population_dict)

        # for data where the city is a child of province which is a child of country
        for province in child.getiterator('province'):
            update_population_dictionary(country_name, province, year_population_dict)


    population_series = pd.Series(year_population_dict[year]).sort_values(ascending=False)
    print('\nThe ' + str(n) + ' cities with the largest population in ' + str(year))
    print(population_series[:n])

#find_n_cities_with_largest_population_for_year(10, 1988)





# Find 10 countries with the lowest infant mortality rates
def find_n_lowest_infant_mortality_countries(n):
    infant_mort_dict = {}
    for child in root:
        im = child.find('infant_mortality')
        # ignore those countries where infant mortality details are not available
        if im is not None:
            country = child.find('name').text
            infant_mortality = im.text
            infant_mort_dict[country] = infant_mortality

    # create series from dictionary
    infant_mort_series = pd.Series(infant_mort_dict).sort_values()
    print('\nThe ' + str(n) + ' countries with the lowest infant mortality rates')
    print(infant_mort_series[:n])

#find_n_lowest_infant_mortality_countries(10)

