import pandas as pd
import json
from pandas.io.json import json_normalize


# Using data in file 'data/world_bank_projects.json' and the techniques demonstrated above,
# Find the 10 countries with most projects
# Find the top 10 major project themes (using column 'mjtheme_namecode')
# In 2. above you will notice that some entries have only the code and the name is missing. Create a dataframe with the missing names filled in.

json_df = pd.read_json('data/world_bank_projects.json')
project_theme_dict = {}
#Find the top 10 major project themes (using column 'mjtheme_namecode')

def find_top_major_project_themes(n):

    str_json = json.load((open('data/world_bank_projects.json')))
    normalized_df = json_normalize(str_json, 'mjtheme_namecode')

    # remove duplicates
    deduped_df = normalized_df.drop_duplicates()

    # create a dictionary of theme code and name
    project_theme_dict = {}
    for index, row in deduped_df.iterrows():
        theme_name = row['name']
        if(len(theme_name) > 0):
            project_theme_dict[row['code']] = theme_name

    theme_code_series = json_df['mjtheme_namecode']
    for item in theme_code_series.iteritems():
        theme_list = item[1]
        for theme in theme_list:
            theme_name = theme['name']
            if (len(theme_name) == 0):
                theme_code = theme['code']
                theme['name'] = str(project_theme_dict[theme_code])

    # print(json_df['mjtheme_namecode'].value_counts()[:10])

    # json_df['mjtheme_namecode'] = theme_code_series
    # print(json_df['mjtheme_namecode'].value_counts()[:10])
    #print(theme_code_series)

    str_json = json_df.to_string()
    normalized_df = json_normalize(str_json, 'mjtheme_namecode')
    print('\n\n' + str(normalized_df.code.value_counts()[:10]))
    #print(normalized_df['mjtheme_namecode'].value_counts()[:10])

find_top_major_project_themes(10)


#Find the 10 countries with most projects
def find_top_countries_with_most_projects(n):
    country_project_series = json_df['countryshortname']
    print(country_project_series.value_counts()[:n])

find_top_countries_with_most_projects(5)
