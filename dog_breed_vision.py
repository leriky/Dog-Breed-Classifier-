import io
import os
# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types
from flask import Flask, render_template, request

from flask_uploads import UploadSet, configure_uploads, IMAGES



os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= "***********"
app = Flask(__name__)

photos = UploadSet('photos', IMAGES)

app.config['UPLOADED_PHOTOS_DEST'] = 'static/img'
configure_uploads(app, photos)
# def model(filename):
#     #google.io stuff
#     return answer



###AUTOM ML VISION



def predict(file_path):
    project_id = "*************"
    model_id = "******************"

    """Predict."""
    # [START automl_vision_classification_predict]
    from google.cloud import automl
    prediction_client = automl.PredictionServiceClient()

    # Get the full path of the model.
    model_full_id = prediction_client.model_path(
        project_id, "us-central1", model_id
    )

    # Read the file.
    with io.open(file_path, "rb") as content_file:
        content = content_file.read()

    image = automl.types.Image(image_bytes=content)
    payload = automl.types.ExamplePayload(image=image)

    # params is additional domain-specific parameters.
    # score_threshold is used to filter the result
    # https://cloud.google.com/automl/docs/reference/rpc/google.cloud.automl.v1#predictrequest
    params = {"score_threshold": "0.6"}

    response = prediction_client.predict(model_full_id, payload, params)
    return response.payload


    # print("Prediction results:")
    # for result in response.payload:
    #     print("Predicted class name: {}".format(result.display_name))
    #     print("Predicted class score: {}".format(result.classification.score))
    # [END automl_vision_classification_predict]

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'photo' in request.files:

        filename = photos.save(request.files['photo'])
        full_path = os.path.join(app.config['UPLOADED_PHOTOS_DEST'], filename)

        labels = predict(full_path)

        predictions = []
        predictions2 =[]

        for label in labels:
                predictions.append(label.display_name)  #make a list as print would only show up in terminal

        for label in labels:
            predictions2.append(label.classification.score)

        def return_string(list_item):
            for word in list_item:
                return word

        prediction_text = "the predicted dog breed is {} and the probability score is {}"\
        .format(return_string(predictions), round(return_string(predictions2),2))
    else:
        prediction_text = "nothing to predict yet.."

    return render_template('upload.html',  prediction_text= prediction_text)

if __name__ == '__main__':
    app.run(debug=False)






