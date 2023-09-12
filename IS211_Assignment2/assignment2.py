import argparse
import urllib.request
import logging
import datetime

logging.basicConfig(filename='errors.log', level=logging.ERROR)
logger = logging.getLogger('assignment2')

def downloadData(url):
    """Downloads the data"""
    with urllib.request.urlopen(url) as response:
        return response.read().decode('utf-8') 
        #  Downloads data from the specified URL, 
        # returns the content of the response as a UTF-8 decoded string.

def processData(file_content):    
    data_dict = {} 
    # to store processed data
    lines = file_content.strip().split('\n')[1:] 
    #  splits the file content into lines skipping first (headers)
    
    for idx, line in enumerate(lines, 1): 
        # for each line
        id, name, birthday_str = line.split(',')
        # grab the id, name, and birthday
        try:
            day, month, year = map(int, birthday_str.split('/'))
            # tries to get the day, month, year 
            birthday = datetime.date(year, month, day)
            # makes datetime.object
            data_dict[int(id)] = (name, birthday)
            # stores data in data_dict 
        except (ValueError, IndexError):
            logger.error(f"Error processing line #{idx} for ID #{id}")
            # the birthdays may mess up, so this logs those
            
    return data_dict
    

def displayPerson(id, personData):
    if id in personData:
        # if the id is valid
        name, birthday = personData[id]
        # grab the name and birthday
        print(f"Person #{id} is {name} with a birthday of {birthday.strftime('%Y-%m-%d')}")
        # print out the info
    else:
        print(f"No user found with that id")
    

def main(url):
    print(f"Running main with URL = {url}...")
    csvData = downloadData(url)
    personData = processData(csvData)
    while True:
        try:
            user_id = int(input("Please enter an ID to look up: "))
            # ask for id to lookup
            if user_id <= 0:
                # if its 0 or -negative
                print("Exiting...")
                break
            displayPerson(user_id, personData)
            # otherwise give the data
        except ValueError:
            print("Please enter a valid integer ID.")
            # make sure its a number

if __name__ == "__main__":
    """Main entry point"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    main(args.url)


