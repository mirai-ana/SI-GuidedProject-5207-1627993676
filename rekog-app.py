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
    bucket="intelligent-album"
    collection_id= "Intelligent-Album-Faces"
    filename=filepath
    relative_filename=os.path.split(filepath)[1]
    fileNames=[relative_filename]
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

dataset="https://www.kaggle.com/rathimadhav/intelligent-album-manager"
#Create bucket from link
#Create collection in rekog
#List faces
