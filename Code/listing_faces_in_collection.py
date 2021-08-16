import boto3
import csv

client = boto3.client('rekognition',
                      aws_access_key_id ="AKIAVSOODXZIHUYFZX7X",
                      aws_secret_access_key ="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",
                      region_name ='us-east-1'
                        )

def list_faces_in_collection(collection_id):
    
    maxResults=2
    faces_count=0
    tokens=True
    
    response=client.list_faces(CollectionId=collection_id,
                               MaxResults=maxResults)
                                  
    print('Faces in collection : ' + collection_id)
    
    while tokens:
        faces=response['Faces']
        for face in faces:
            print("Face Id     : "  + face["FaceId"])
            print("External Id : " + face["ExternalImageId"])
            faces_count+=1
            
        if 'NextToken' in response:
            nextToken=response['NextToken']
            response=client.list_faces(CollectionId=collection_id,
                                       NextToken=nextToken,MaxResults=maxResults)
        else:
            tokens=False
    return faces_count

def main():
    bucket = 'intelligentalbum'
    collection_id = 'intelligent_Album_M'
    
    faces_count=list_faces_in_collection(collection_id)
    print("faces count: " + str(faces_count))
    
if __name__=="__main__":
    main()

