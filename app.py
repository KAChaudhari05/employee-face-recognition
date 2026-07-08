import boto3
import json
import os


AWS_REGION = "ap-south-1"

BUCKET_NAME = "employee-face-images-khushi"

IMAGE_PATH = "images/employee1.jpg"


s3_client = boto3.client(
    "s3",
    region_name=AWS_REGION
)


rekognition_client = boto3.client(
    "rekognition",
    region_name=AWS_REGION
)



# Upload image to S3

file_name = os.path.basename(IMAGE_PATH)


print("Uploading image...")


s3_client.upload_file(
    IMAGE_PATH,
    BUCKET_NAME,
    file_name
)


print("Upload completed")



# Detect faces


response = rekognition_client.detect_faces(

    Image={
        "S3Object":{
            "Bucket":BUCKET_NAME,
            "Name":file_name
        }
    },

    Attributes=[
        "ALL"
    ]

)



faces = response["FaceDetails"]



print("-----------------------")

print(
    "Number of Faces:",
    len(faces)
)



face_results=[]


for index,face in enumerate(faces):

    confidence = face["Confidence"]

    print(
        f"Face {index+1} Confidence:",
        confidence
    )


    face_results.append(
        {
            "face_number":index+1,
            "confidence":confidence
        }
    )



# Save result.json


result = {

    "image":file_name,

    "number_of_faces":len(faces),

    "faces":face_results

}



with open(
    "result.json",
    "w"
) as f:

    json.dump(
        result,
        f,
        indent=4
    )


print("result.json created")
