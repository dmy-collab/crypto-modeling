# the link to original article https://nealcaren.org/lessons/twint/

from datetime import timedelta
from string import ascii_letters, digits
from os import mkdir, path
import pandas as pd
import twint


# The cell below creates several functions to automate the process of searching over several days and storing each
# day’s results as distinct json file: twint_loop splits the date range into a series of days and calls twint_search
# to do the searching for each date. Each json is named after the date and stored in a directory based on the search
# term, using clean_name to ensure that it is a valide directory name. The date loop


def clean_name(dirname):
    valid = set(ascii_letters + digits)
    return ''.join(a for a in dirname if a in valid)


def twint_search(searchterm, since, until, json_name):
    '''
    Twint search for a specific date range.
    Stores results to json.
    '''
    c = twint.Config()
    c.Search = searchterm
    c.Since = since
    c.Until = until
    c.Hide_output = True
    c.Store_json = True
    c.Output = json_name
    c.Debug = True

    try:
        twint.run.Search(c)
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        print("Problem with %s." % since)


def twint_loop(searchterm, since, until):

    dirname = clean_name(searchterm)
    try:
        # Create target Directory
        mkdir(dirname)
        print("Directory", dirname, "Created ")
    except FileExistsError:
        print("Directory", dirname, "already exists")

    daterange = pd.date_range(since, until)

    for start_date in daterange:

        since = start_date.strftime("%Y-%m-%d")
        until = (start_date + timedelta(days=1)).strftime("%Y-%m-%d")  # timeframe splitting days

        json_name = '%s.json' % since
        json_name = path.join(dirname, json_name)

        print('Getting %s ' % since)
        twint_search(searchterm, since, until, json_name)


twint_loop('#hodl', '06-01-2021', '07-01-2021')  # my keywords and timeframes

from glob import glob  # The glob module finds all the pathnames matching a specified pattern
# according to the rules used by the Unix shell, although results are returned in arbitrary order.

#separate data files can be combined into a single dataframe:
file_names = glob(path.join('hodl','*.json'))
dfs = [pd.read_json(fn, lines = True) for fn in file_names]
wm2018_df = pd.concat(dfs)

wm2018_df.info()