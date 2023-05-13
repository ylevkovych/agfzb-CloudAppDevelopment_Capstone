/**
  *
  * main() will be run when you invoke this action
  *
  * @param Cloud Functions actions accept a single parameter, which must be a JSON object.
  *
  * @return The output of this action, which must be a JSON object.
  *
  */
  
  
const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');
 

function uuidv4() {
  return ([1e7]+-1e3+-4e3+-8e3+-1e11).replace(/[018]/g, c =>
    (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
  );
}  

function main(params) {
	const authenticator = new IamAuthenticator({ apikey: "9TTHdpmAE8OU2xEc4cu3xPswTWTyyEMUeUO2O1px9b_I" })
    const cloudant = CloudantV1.newInstance({
      authenticator: authenticator
    });
    cloudant.setServiceUrl("https://b1f76e64-470e-4fa9-92ce-22c7f524bbc4-bluemix.cloudantnosqldb.appdomain.cloud");

    let review = params.review;
    review.id = uuidv4();
    
    cloudant.postDocument({
        db: "reviews",
        document: review,
    })
      .then((result) => {
        let code = 201;
        resolve({
          statusCode: code,
          headers: { "Content-Type": "application/json" },
          body: {"msg": "Success"}
        });
      })
      .catch((err) => {
        reject(err);
      });
}

    

