# doing necessary imports
from flask import Flask, make_response, request
from flask_cors import cross_origin
import json
from Requests import ApiRequests
from pymongo import MongoClient
from Chats import Chats
from EmailSend import EmailPrep


def DataBaseConfiguration():
    mongo_client = MongoClient(
        "mongodb+srv://emergingtechchatbot:chatbotemergingtech@cluster0.wggca.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    return mongo_client.get_database('covid19DB')


def APIRequest(query):
    api = ApiRequests.ApiRequests()
    print("@@@ query", query)
    if query == "world":
        return api.WorldwideAPI()
    else:
        return api.CountryWiseAPI(query)


def prepareEmail(contact_list):
    client = EmailPrep.MailClient()
    client.sendEmail(contact_list)


bot_app = Flask(__name__)  # to initialize flask with the name app

# Dialog Flow - Python connection
@bot_app.route('/webhook', methods=['POST'])
@cross_origin()
def webhook():
    req = request.get_json(silent=True, force=True)
    # print(req)
    # return{
    #     'fulfillmentText' : 'Hello from the other side.'
    # }
    response = requestProcess(req)
    response = json.dumps(response, indent=4)
    print(response)
    responseHeader = make_response(response)
    responseHeader.headers['Content-Type'] = 'application/json'
    return responseHeader


# Dialog Flow Requests
def requestProcess(request):
    dialog_Flow = Chats.Log()
    id_session = request.get('responseId')
    dialog_result = request.get("queryResult")
    dialog_intent = dialog_result.get("intent").get('displayName')
    dialog_query_text = dialog_result.get("queryText")
    param = dialog_result.get("parameters")
    user_name = param.get("cust_name")
    user_contact = param.get("cust_contact")
    user_email = param.get("cust_email")
    database = DataBaseConfiguration()

    if dialog_intent == 'countryBasedSearch':
        country = param.get("geo-country")
        if country == "United States":
            country = "USA"

        dialog_fulfillment, deaths_no, tests_no = APIRequest(country)
        response = "COVID REPORT in \"" + country + "\" \n\n" + \
                          " \t TOTAL :\n"+ \
                   country +"'s Total no. of Deaths : " + str(deaths_no.get('total')) + "\n" + \
                   country +"'s Total no. of  cases : " + str(dialog_fulfillment.get('total')) + "\n" + \
                   country +"'s Total  no. of Tests Done : " + str(tests_no.get('total'))+\
                            "\n\t RECENT: \n"+\
                          country +"'s Recent cases :" + str(dialog_fulfillment.get('new')) + "\n" + \
                          country +"'s Active cases : " + str(dialog_fulfillment.get('active')) + "\n" + \
                          country +"'s Critical cases : " + str(dialog_fulfillment.get('critical')) + "\n" + \
                          country +"'s Recovered cases : " + str(dialog_fulfillment.get('recovered')) + "\n" + \
                          country +"'s Latest Deaths : " + str(deaths_no.get('new')) + "\n"
        print(response)
        dialog_Flow.saveChats(id_session, country, response, dialog_intent, database)
        dialog_Flow.save_cases("country", dialog_fulfillment, database)

        return {

            "fulfillmentMessages": [
                {
                    "text": {
                        "text": [
                            response
                        ]

                    }
                },
                {
                    "text": {
                        "text": [
                            "Want this report send to your email? \n "
                            "1. Sure \n "
                            "2. Not now "
                        ]

                    }
                }
            ]
        }
    elif dialog_intent == "continueConversation" or dialog_intent == "Welcome" or dialog_intent == "notSendEmail" or \
            dialog_intent == "endConversation" or dialog_intent == "Fallback" or \
            dialog_intent == "FAQ" or dialog_intent == "selectCountryOption":
        dialog_fulfillment = dialog_result.get("fulfillmentText")
        dialog_Flow.saveChats(id_session, dialog_query_text, dialog_fulfillment, dialog_intent, database)

    elif dialog_intent == "sendEmailReport":
        dialog_fulfillment = dialog_result.get("fulfillmentText")
        dialog_Flow.saveChats(id_session, "Sure send email", dialog_fulfillment, dialog_intent, database)
        val = dialog_Flow.get_cases("country", "", database)
        prepareEmail([user_name, user_contact, user_email, val])

    elif dialog_intent == "TotalCases":
        dialog_fulfillment = APIRequest("world")

        response = "Last updated : " + str(dialog_fulfillment.get('last_update'))+\
                   "\nCOVID-19 World Wide Report \n\n" + \
                   "World Wide Deaths  : " + str(dialog_fulfillment.get('deaths')) + "\n" + \
                   "World Wide Fatality Rate : " + str(dialog_fulfillment.get('fatality_rate') * 100) + "%" + "\n" + \
                   "World Wide Active cases : " + str(dialog_fulfillment.get('active')) + "\n" + \
                   "World Wide Confirmed cases :" + str(dialog_fulfillment.get('confirmed')) + "\n" + \
                   "World Wide Recovered cases : " + str(dialog_fulfillment.get('recovered')) + "\n"
        print(response)
        dialog_Flow.saveChats(id_session, "Cases worldwide", response, dialog_intent, database)
        dialog_Flow.save_cases("world", dialog_fulfillment, database)

        return {

            "fulfillmentMessages": [
                {
                    "text": {
                        "text": [
                            response
                        ]

                    }
                },
                {
                    "text": {
                        "text": [
                            "Want this report send to your email? \n "
                            "\n 1. Sure "
                            "\n 2. Not now "
                        ]

                    }
                }
            ]
        }

    else:
        return {
            "fulfillmentText": "Oops!! Sorry \n Can we Start again.., Please say Hi",
        }

if __name__ == "__main__":
    bot_app.run(port=5000, debug=True)  # running the app on the local machine on port 8000
