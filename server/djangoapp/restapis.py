import requests
import json
from requests.auth import HTTPBasicAuth
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features,SentimentOptions
import time
from .models import CarDealer, DealerReview


def get_request(url, **kwargs):
    
    try:
        api_key = kwargs.get("api_key")

        if api_key:
            params = dict()
            params["text"] = kwargs["text"]
            params["version"] = kwargs["version"]
            params["features"] = kwargs["features"]
            params["return_analyzed_text"] = kwargs["return_analyzed_text"]
            response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('api_key', api_key))
        else:
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        print("Network exception occurred")

    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data



# Create a `post_request` to make HTTP POST requests
def post_request(url, payload, **kwargs):
    response = requests.post(url, params=kwargs, json=payload)
    status_code = response.status_code
    print("With status {} ".format(status_code))
    return json.loads(response.text)


def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result and "rows" in json_result.keys():
        # Get the row list in JSON as dealers
        dealers = json_result["rows"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealer_by_id_from_cf(url, id):
    dealer = None
    json_result = get_request(url, id=id)
    if json_result:
        result = json_result[0]
        dealer = CarDealer(address=result["address"], city=result["city"],id=result["id"], lat=result["lat"], long=result["long"], full_name=result["full_name"],short_name=result["short_name"], st=result["st"], zip=result["zip"])
    return dealer


def get_dealer_reviews_from_cf(url, **kwargs):
    results = []
    
    id = kwargs.get("id")
    if id:
        json_result = get_request(url, id=id)
    else:
        json_result = get_request(url)
    
    if json_result:
        reviews = json_result["data"]["docs"]
        for dealer_review in reviews:
            review_obj = DealerReview(dealership=dealer_review["dealership"],
                                   name=dealer_review["name"],
                                   purchase=dealer_review["purchase"],
                                   review=dealer_review["review"],
                                   purchase_date=dealer_review["purchase_date"],
                                   car_make=dealer_review["car_make"],
                                   car_model=dealer_review["car_model"],
                                   car_year=dealer_review["car_year"],
                                   sentiment="")
    
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)

            results.append(review_obj)

    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(text):
    url = "https://api.au-syd.natural-language-understanding.watson.cloud.ibm.com/instances/d46ad751-db72-4820-a4d8-ace969afb937"
    api_key = "t2NQKC6RRNyiJClBeLJZ1d83U5dI9xdu68Vt4p3QWbAi"

    nlu = NaturalLanguageUnderstandingV1(version='2021-08-01',
                                authenticator=IAMAuthenticator(api_key))
    nlu.set_service_url(url)

    text = text+"abra cad abra"
    response = nlu.analyze( text=text,features=Features(sentiment=SentimentOptions(targets=[text]))).get_result()

    return json.dumps(response, indent=2)['sentiment']['document']['label']




