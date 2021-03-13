import urllib 
import json
import os
import io

import torch
from PIL import Image
from torchvision import models, transforms
import torch.nn.functional as F


model = models.squeezenet1_1()
model.load_state_dict(torch.load("model/squeezenet1_1-f364aa15.pth"))
model.eval()

normalize = transforms.Normalize(
    mean=[0.485, 0.456, 0.406],
    std=[0.229, 0.224, 0.225]
)

snet_transform = transforms.Compose([transforms.Resize(224),
                                       transforms.CenterCrop(224),
                                       transforms.ToTensor(), 
                                       normalize])     

json_file = open("model/imagenet_class_index.json")
json_str = json_file.read()
labels = json.loads(json_str) 

def transform_image(image):
    if image.mode != "RGB":
        image = image.convert("RGB")

def lambda_handler(event, context):
    data = {}
    url = event['queryStringParameters']['url']
    image = Image.open(urllib.request.urlopen(url))
    image = snet_transform(image)
    image = image.view(-1, 3, 224, 224)

    prediction = F.softmax(model(image)[0])
    topk_vals, topk_idxs = torch.topk(prediction, 3)

    data["predictions"] = []

    for i in range(len(topk_idxs)):
        r = {"label": labels[str(topk_idxs[i].item())][1], 
             "probability": topk_vals[i].item()}
        data["predictions"].append(r)    
    return json.dumps(data)