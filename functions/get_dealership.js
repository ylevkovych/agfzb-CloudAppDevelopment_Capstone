
const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

function main(params) {

    const authenticator = new IamAuthenticator({ apikey: "" })
    const cloudant = CloudantV1.newInstance({
      authenticator: authenticator
    });
    cloudant.setServiceUrl("");

    let dbListPromise = null;
    
    
    return params.dealerId || params.state ? getByFilter(cloudant, params) : getAll(cloudant);
}

function getByFilter(cloudant, params) {
    return new Promise((resolve, reject) => {
        
        const selector = { };
        
        if (params.dealerId) {
            selector.id = {
                '$eq': parseInt(params.dealerId)
            };
        }
        
        if (params.state) {
            selector.state = {
                '$eq': params.state    
            };
        }
        
        const docFilter = {
            db: 'dealerships',
            selector: selector
        };
        
        cloudant.postFind(docFilter)
        .then(response => {
            
            let result = response.result;
            
            let code = result.length < 1 ? 404 : 200;
            
            resolve({
                statusCode: code,
                headers: { "Content-Type": "application/json" },
                body: result
            });
        })
        .catch(err => {
            reject({ err: err });
        });
    });    
}

function getAll(cloudant) {
    return new Promise((resolve, reject) => {
        
        const docFilter = {
            db: 'dealerships',
            includeDocs: true
        };
        
        cloudant.postAllDocs(docFilter)
        .then(response => {
            
            let result = response.result.rows;
            
            let code = result.length < 1 ? 404 : 200;
            
            resolve({
                statusCode: code,
                headers: { "Content-Type": "application/json" },
                body: result
            });
        })
        .catch(err => {
            reject({ err: err });
        });
    });    
}


