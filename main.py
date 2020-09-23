import os,json
from fileHelper import getConfig,convertDocuments
from ibm_watson import DiscoveryV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

def uploadFiles (config):
    authenticator = IAMAuthenticator(config["discovery_api_key"])
    discovery = DiscoveryV1(
        version='2019-04-30',
        authenticator=authenticator
        )
    discovery.set_service_url(config["discovery_url"])
    for file in os.listdir(config["conversionDir"]):
            if file.endswith(".pdf"):
                fileName = os.path.join(config["conversionDir"],file)
                with open(fileName,"rb") as fileinfo:
                    print("[File Upload] uploading {0}".format(fileName))
                    add_doc = discovery.add_document(
                        config["discovery_environment_id"], 
                        config["discovery_collection_id"],
                        file=fileinfo).get_result()
                    print(json.dumps(add_doc, indent=2))


config = getConfig()
convertDocuments(config['documentDir'],config['conversionDir'],config['max_file_size'])
print("[Processing Files] Done processing files.")
uploadFiles(config)
print("[File Upload] done Uploading")

