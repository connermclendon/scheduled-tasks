from datetime import datetime
import pandas as pd
import random
import smtplib

# 1. Update with your own email configuration
MY_EMAIL = "connermclendonpython@gmail.com"
MY_PASSWORD = "iksu hrci xsqb vkbt"  # Use an App Password, not your normal password

# 2. Set up today's date
today = datetime.now()
today_tuple = (today.month, today.day)

# 3. Read the birthdays.csv file
# The CSV should have columns: name, email, year, month, day
try:
    data = pd.read_csv("birthdays.csv")
except FileNotFoundError:
    print("Error: birthdays.csv not found.")
    data = pd.DataFrame()

# 4. Create a dictionary from the dataframe
birthdays_dict = {
    (data_row["month"], data_row["day"]): data_row
    for (index, data_row) in data.iterrows()
}

# 5. Check if today matches a birthday in the CSV
if today_tuple in birthdays_dict:
    person_data = birthdays_dict[today_tuple]

    # Pick a random letter template
    file_path = f"letter_templates/letter_{random.randint(1, 3)}.txt"
    with open(file_path) as letter_file:
        contents = letter_file.read()
        # Replace the placeholder with the person's actual name
        message = contents.replace("[NAME]", person_data["name"])

    # 6. Send the email via SMTP using SSL (Port 465)
    try:
        # SMTP_SSL is more secure and less prone to dropping connections
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as connection:
            connection.login(MY_EMAIL, MY_PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=person_data["email"],
                msg=f"Subject:Happy Birthday!\n\n{message}"
            )
        print(f"Birthday email successfully sent to {person_data['name']}!")
    except Exception as e:
        print(f"Failed to send email: {e}")

else:
    print("No birthdays today.")


