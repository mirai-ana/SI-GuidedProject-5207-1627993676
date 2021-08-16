import os
from flask import Flask , request, render_template
from gevent.pywsgi import WSGIServer
import boto3
import csv

with open("new_user_credentials.csv",'r') as input:
    next(input)
    reader =csv.reader(input)
    for line in reader:
        access_key_id =line[0]
        secret_access_key =line[1]
        
client = boto3.client('rekognition',
                      aws_access_key_id ="AKIAVSOODXZIHUYFZX7X",
                      aws_secret_access_key ="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",
                      region_name ='us-east-1'
                        )
        
s3 = boto3.client('s3',
                  aws_access_key_id ="AKIAVSOODXZIHUYFZX7X",
                  aws_secret_access_key ="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",
                  region_name ='us-east-1'
                  )

app = Flask(__name__)

def main(filepath):
    bucket = 'intelligentalbum'  #our bucket name in S3
    collection_id = 'intelligent_Album_M' #Our collection name of reference faces
    
    filename = filepath #filepath of uploaded img file by user, passed as an arguement
    
    relative_filename = os.path.split(filepath)[1] #the is the name of the file , eg: "test1.jpg"
    #print(relative_filename)
    
    fileNames = [relative_filename] 
  
    s3.upload_file(filename, bucket, relative_filename)  #uplaoding the file in S3 bucket
    print("file Uploaded")
    
    threshold = 70
    maxFaces = 2

    #finding the face in uploaded image in the reference
    for fileName in fileNames:
        response=client.search_faces_by_image(CollectionId=collection_id,
                                              Image={'S3Object':
                                                     {'Bucket':bucket,
                                                      'Name':fileName}},
                                              FaceMatchThreshold=threshold,
                                              MaxFaces=maxFaces)
        recognized_person_name = "Not Detected"    
        #printing the matched face details in console only    
        faceMatches=response['FaceMatches']
        print ('Matching faces')
        for match in faceMatches:
            print ('FaceId:' + match['Face']['FaceId'])
            print ('External Id:' + match['Face']["ExternalImageId"])
            print ('Similarity: ' + "{:.2f}".format(match['Similarity']) + "%")
            
            #to move the file wihtin s3 bucket, from the bucket to respective folder
            copy_from = str(bucket+'/'+fileName)  
            move_to = str(match['Face']["ExternalImageId"][:-4]+'/'+fileName)
            recognized_person_name = str(match['Face']["ExternalImageId"][:-4])
            s3.copy_object(Bucket=bucket, CopySource=copy_from, Key=move_to)
             
            print("successfully moved to " + move_to)
        return recognized_person_name  #returning the name of the person whose face was detected
                                        #to be used by flask app, to print on the web page.
        
        
#opening up the base html template. 
@app.route('/')
def index():
    return render_template('base.html')

#whenever the predict button is clicked, the chosen file is uplaoded to uploads folder
#it then calls our main function, psases the uploaded file's path as arguement, and print's the
#returned name as output on web screen
@app.route('/predict',methods = ['GET','POST'])
def upload():
    if request.method == 'POST':
        f = request.files['image']
        print("current path")
        basepath = os.path.dirname(__file__)
        print("current path", basepath)
        filepath = os.path.join(basepath,'uploads',f.filename)
        print("upload folder is ", filepath)
        f.save(filepath)
        
        text = main(filepath) #calling our main function, passing stored file's
                                #filepath as arguement to it
    return text
    
if __name__ == '__main__':
    app.run(debug = True, threaded = False)
        
        
        
    
    
    