
const { Cloudant } = require('@cloudant/cloudant'); 

function main(params) {

    cloudant_params = {
        "URL": "https://b1f76e64-470e-4fa9-92ce-22c7f524bbc4-bluemix.cloudantnosqldb.appdomain.cloud",
        "IAM_API_KEY": "9TTHdpmAE8OU2xEc4cu3xPswTWTyyEMUeUO2O1px9b_I"
    };

    return new Promise(function (resolve, reject) {
        
        const cloudant = Cloudant({
            url: cloudant_params.URL,
            plugins: {iamauth: {iamApiKey:cloudant_params.IAM_API_KEY}} 
        });

        const dbconn = cloudant.use('dealerships'); 
        
        if (params.state) { 
            dbconn.find({"selector": {"state": {"$eq": params.state}}}, 
                function (err, result) { 
                    if (err) { 
                        reject(err); 
                    } 

                    let code = result.docs.length==0 ? 404 : 200; 
                    
                    resolve({ 
                        statusCode: code, 
                        headers: {'Content-Type': 'application/json'}, 
                        body: result 
                    }); 
                }
            ); 
        } else { 
            dbconn.list({ include_docs: true }, 
                function (err, result) { 
                    if (err) { 
                        reject(err); 
                    } 

                    let code = result.docs.length==0 ? 404 : 200; 

                    resolve({ 
                        statusCode: code, 
                        headers: { 'Content-Type': 'application/json' }, 
                        body: result 
                    }); 
                }
            ); 
        } 
    });
}