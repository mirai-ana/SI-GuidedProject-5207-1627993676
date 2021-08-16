import boto3
import csv
        
client = boto3.client('rekognition',
                      aws_access_key_id ="AKIAVSOODXZIHUYFZX7X",
                      aws_secret_access_key ="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",
                      region_name ='us-east-1'
                        )

def create_collection(collection_id):
    
    print('Creating collection:' + collection_id)
    
    response=client.create_collection(CollectionId=collection_id)
    
    print('Collection ARN: ' + response['CollectionArn'])
    print('Status code: ' + str(response['StatusCode']))
    print('Done...')
    
def main():
    collection_id='intelligent_Album_M'
    create_collection(collection_id)
    
if __name__=="__main__":
    main()