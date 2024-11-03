#!/usr/bin/env python3

import requests
import argparse

# Define the base URL and initial id
base_url = "https://artemis.ase.in.tum.de/api/"
# Parse command-line arguments
parser = argparse.ArgumentParser(description="Scrape course data from Artemis.")
parser.add_argument(
    "jwt",
    type=str,
    help="The JWT token for authentication (copy it from any artemis requests)",
)
parser.add_argument("start_id", type=int, help="The minimum ID a course could have")
parser.add_argument("max_id", type=int, help="The maximum ID a course could have")
args = parser.parse_args()

start_id = args.start_id
max_id = args.max_id
jwt_token = args.jwt

# Define your cookies as a dictionary
cookies = {
    "jwt": jwt_token,
}

# Ensure the courses.txt file is empty before writing
with open("courses.txt", "w") as file:
    file.write("")

# Loop through the range of IDs
for course_id in range(start_id, max_id + 1):
    # Construct the full URL
    url = f"{base_url}courses/{course_id}/for-dashboard"

    try:
        # Make a GET request with cookies
        response = requests.get(url, cookies=cookies)

        # Check if the request was successful
        if response.status_code == 200:
            # Extract the course ID and title from the response
            course_data = response.json().get("course", {})
            course_id = course_data.get("id")
            course_title = course_data.get("title")

            # Write the course ID and title to the file
            with open("courses.txt", "a") as file:
                file.write(
                    f"Course ID: {course_id}, Title: {course_title}, Url: https://artemis.ase.in.tum.de/courses/{course_id}\n"
                )

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
