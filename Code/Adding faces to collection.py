import boto3
import csv

client = boto3.client('rekognition',
                      aws_access_key_id ="AKIAVSOODXZIHUYFZX7X",
                      aws_secret_access_key ="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",
                      region_name ='us-east-1')
                        

def add_faces_to_collection (bucket,photo,collection_id):
    
    response = client.index_faces(CollectionId=collection_id,
                                  Image={'S3Object':{'Bucket':bucket,'Name':photo}},
                                  ExternalImageId=photo,
                                  MaxFaces=2,
                                  QualityFilter="AUTO",
                                  DetectionAttributes=['ALL'])
    
    print ('Results for ' + photo)
    print('Face indexed:')
    for faceRecord in response['FaceRecords']:
        print(' Face ID: ' + faceRecord['Face']['FaceId'])
        print(' External Id: ' + faceRecord['Face']["ExternalImageId"])
        print(' Location: {} ' .format(faceRecord['Face']['BoundingBox']))
        
        
    print('Faces not indexed:')
    for unindexedFace in response['UnindexedFaces']:
        print(' Location: {}'.format(unindexedFace['FaceDetail']['BoundingBox']))
        print(' Reasons:')
        for reason in unindexedFace['Reasons']:
            print('  ' + reason)
            
    return len(response ['FaceRecords'])


def main():
    
    bucket = 'intelligentalbum'
    collection_id='intelligent_Album_M'
    
    photos = ["test1.jpg","test2.jpg","test3.jpg","test4.jpg","test5.jpg"]
    
    for photo in photos:
        indexed_faces_count = add_faces_to_collection (bucket, photo, collection_id)
        print("Faces indexed count:" + str(indexed_faces_count))
        
if __name__ == "__main__":
    main()

        
        