FROM public.ecr.aws/lambda/python:3.8

COPY app.py requirements.txt ./

RUN python3.8 -m pip install -r requirements.txt -t .

RUN mkdir model
RUN curl https://download.pytorch.org/models/squeezenet1_1-f364aa15.pth -o ./model/squeezenet1_1-f364aa15.pth
COPY imagenet_class_index.json ./model/imagenet_class_index.json

CMD ["app.lambda_handler"]

