from cloudant.client import Cloudant
from cloudant.error import CloudantException


def main(dict):
    secret = {
        "URL": "https://b1f76e64-470e-4fa9-92ce-22c7f524bbc4-bluemix.cloudantnosqldb.appdomain.cloud",
        "IAM_API_KEY": "9TTHdpmAE8OU2xEc4cu3xPswTWTyyEMUeUO2O1px9b_I",
        "ACCOUNT_NAME": "b1f76e64-470e-4fa9-92ce-22c7f524bbc4-bluemix"
    }

    client = Cloudant.iam(
        account_name=secret["ACCOUNT_NAME"],
        api_key=secret["IAM_API_KEY"],
        url=secret["URL"],
        connect=True,
    )

    dbconn = client["reviews"]

    try:
        selector = {'dealership': {'$eq': int(dict["dealerId"])}}
        data = dbconn.get_query_result(selector, raw_result=True)

        result = {
            'headers': {'Content-Type': 'application/json'},
            'body': {'data': data}
        }
    except:
        result = {
            'statusCode': 500,
            'message': "Something went wrong"
        }
    
    return result