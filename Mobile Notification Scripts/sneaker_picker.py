
#---------------------------------------#
#RANDOMLY PICK A SHOE FOR ME TO WEAR#
#SENDS SMS VIA Twillo#
#SEND AUTOMATED SMS MESSAGES VIA TEXT
#---------------------------------------#

import sys
import random
import csv
import time
import schedule

from twilio.rest import Client
final_sneaker_list = []

account_sid = "ACf5e008186ee5b6359b95794fbb6d2898"
auth_token = "89013053222d7b00129e0f90f26f6d60"

client = Client(account_sid, auth_token)


def sneaker_ranomizer(file):

    with open(file) as f:
        sneaker_list = f.readlines()

    for entry in sneaker_list:
        final_sneaker_list.append(entry.strip('\n'))

    return random.choice(final_sneaker_list)


def notifications(sneaker):
    message = client.messages \
        .create(
             body='Hello Jonathan, wear this today: ' + str(sneaker) + '!',
             from_='+12039025254',
             to='+13018288246'
         )

#CURRENRTLY WORKING ON THIS SECTION FOR CONSISTENTLY SCHEDULING THE SCTIPT TO EXECUTE#
def main(file):
    sneaker = sneaker_ranomizer(file)
    notifications(sneaker)

if __name__ == '__main__':
    main(sys.argv[1])

schedule.every().day.at('18:41').do(main(file))

while True:
    schedule.run_pending()
    time.sleep(1)
    file = sys.argv[1]
