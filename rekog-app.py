import os
from flask import Flask, request, render_template
from gevent.pywsgi import WSGIServer
import boto3
import csv

with open("credentials.csv",mode="r") as input:
	next(input)
	render=csv.reader(input)
	for line in reader:
		access_key_id=line[0]
		secret_access_key=line[1]
		session_token=line[2]

dataset="https://www.kaggle.com/rathimadhav/intelligent-album-manager"
bucket="intelligent-album"
collection_id= "Intelligent-Album-Faces"

client=boto3.client("rekognition",
					aws_access_key_id=access_key_id,
					aws_secret_access_key=secret_access_key,
					aws_session_token=session_token,
					region_name="ap-south1")

s3=boto3.client("s3",
				aws_access_key_id=access_key_id,
				aws_secret_access_key=secret_access_key,
				aws_session_token=session_token,
				region_name='ap-south1')

app=Flask(__name__)

def create_collection(collection_id):
	print("Creating a collection ""+collection_id)
	response=client.create_collection(CollectionId=collection_id)
	print("Collection ARN: "+response['CollectionArn']+ "\nStatus Code"+str(response['Status Code'])+"\nDone....")

def add_faces_to_collection(bucket,photo,collection_id):
    response=client.index_faces(CollectionId=collection_id,
                                Image={ "S3Object":
                                {"Bucket":bucket,
                                "Name":FileName}},
                                ExternalImageId=photo,
                                MaxFaces=1,
                                QualityFilter= "AUTO",
                                DetectionAttributes=['ALL'])
    print("Results for "+photo+ "\nFaces Indexed:")
    for faceRecord in response["FaceRecords"]:
        print("FaceId:"+faceRecord["Face"]["FaceId"]+"\nExternalId: "+faceRecord["Face"]["ExternalImageId"]+ "Location: {}".format(faceRecord["Face"]["BoundingBox"]))
        print("Faces Not Indexed: ")
    for unindexedFace in response["UnindexedFaces"]:
        print("Location: {}".format(unindexedFace["Face"]["BoundingBox"]))
        print("Causes:"
        for reason in unindexedFace["Reasons"]:
            print("\t"+reason)
    return len(response["FaceRecords"])

def list_faces_in_collection(collection_id):
    maxResults=2
    faces_count=0
    tokens=True
    response=client.list_faces(CollectionId=collection_id,MaxResults=maxResults)
    
    print("Faces in collection:"+collection_id)
    
    while tokens:
        faces=response["Faces"]
        for face in faces:
            print("Face Id:\t"+face["FaceId"]+"\nExternal Id"+face["ExternalImageId"]
            faces_count+=1
        if "NextToken" in response:
            nextToken=response["NextToken"]
            response=client.list_faces(CollectionId=collection_id, NextToken=nextToken, MaxResults=maxResults)
        else:
            tokens=False
    return faces_count

@app.route("/")
def index():
	return render_template('index.html')

@app.route("/predict",methods=["GET", "POST"])
def upload():
	if request.method == "POST":
		f=request.files["image"]
		print("current path")
		basepath=os.path.join(basepath,"uploads",f.filename)
		print("upload file folder is ",filepath)
		f.save(filepath)
		text=main(filepath)
	return text

def main():
    create_collection(collection_id)
    filename=filepath
    relative_filename=os.path.split(filepath)[1]
    fileNames=[relative_filename]
    
    print("Face Count:"+str(list_faces_in_collection(collection_id)))
    photos=[]
    for photo in photos:
        print("Faces Indexed count: "+str(add_faces_to_collection(bucket,photo,collection_id)))

    s3.upload_file(filename, bucket, relative_filename)
    print("File upload")

    threshold=70
    maxFaces=2

    for FileName in fileNames:
        response=client.search_by_faces_by_image(CollectionId=collection_id,
                                                Image={ "S3Object":
                                                    {"Bucket":bucket,
                                                    "Name":FileName}},
                                                FaceMatchThreshold=threshold,
                                                MaxFaces=maxFaces)

        faceMatches=response["FaceMatches"]
        print("Matching faces")
        for match in faceMatches:
            print("FaceId:"+match["Face"]["FaceId"]+"\nExternalId:"+match["Face"]["ExternalImageId"])+"\nSimilarity:"+ "{:.2f}".format(match["Similarity"])+"%")
            
            copy_from = str(bucket+"/"+fileName)
            move_to=str(match["Face"]["ExternalImageId"][:-4]+"/"+fileName)
            recognized_person_name=str(match["Face"]["ExternalImageId"][:-4])
            s3.copy_object(Bucket=bucket, CopySource=copy_from, Key=move_to)
            print("Successfully moved to "+move_to)
        return recognized_person

if __name__ == "main":
	app.run(debug=False, threaded=False)
#Create bucket from link
#Create collection in rekog
#List faces
