import argparse
import urllib.request
import os
import csv
import re
from collections import defaultdict
from datetime import datetime

def downloadData(url):
    if os.path.exists(url):
        with open(url, 'r') as file:
            return file.read()
    else:
        response = urllib.request.urlopen(url)
        return response.read().decode('utf-8')

def processData(file_content):
    data = []
    lines = file_content.splitlines()
    reader = csv.reader(lines)
    for row in reader:
        data.append(tuple(row))
    return data

def count_image_hits(data):
    image_pattern = re.compile(r"\.(jpg|gif|png)$", re.I)
    image_count = sum(1 for row in data if image_pattern.search(row[0]))
    total_count = len(data)
    image_percentage = (image_count / total_count) * 100
    return image_percentage

def popular_browser(data):
    browsers_patterns = {
        "Firefox": re.compile(r"Firefox"),
        "Chrome": re.compile(r"Chrome"),
        "Internet Explorer": re.compile(r"MSIE"),
        "Safari": re.compile(r"Safari")
    }
    
    browser_counts = defaultdict(int)
    for row in data:
        user_agent = row[2]
        for browser, pattern in browsers_patterns.items():
            if pattern.search(user_agent):
                browser_counts[browser] += 1
                break
    most_popular = max(browser_counts, key=browser_counts.get)
    return most_popular, browser_counts

def hits_by_hour(data):
    hour_counts = defaultdict(int)
    for i in range(24): 
        hour_counts[i] = 0
        
    for row in data:
        date_str = row[1]
        date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        hour = date_obj.hour
        hour_counts[hour] += 1
        
    sorted_hours = sorted(hour_counts.items(), key=lambda x: x[1], reverse=True)
    return sorted_hours

def main(url):
    file_content = downloadData(url)
    weblog_data = processData(file_content)

    image_percentage = count_image_hits(weblog_data)
    print(f"Image requests account for {image_percentage:.2f}% of all requests.")

    most_pop_browser, browser_counts = popular_browser(weblog_data)
    print(f"The most popular browser is {most_pop_browser} with {browser_counts[most_pop_browser]} hits.")

    hourly_hits = hits_by_hour(weblog_data)
    for hour, hits in hourly_hits:
        am_pm = "AM" if hour < 12 else "PM"
        hour_12 = hour % 12
        hour_12 = 12 if hour_12 == 0 else hour_12 
        print(f"Hour {hour:02} (24-hour) / {hour_12} {am_pm} (12-hour) has {hits} hits.")
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="Path to the datafile or URL", type=str, required=True)
    args = parser.parse_args()
    main(args.url)