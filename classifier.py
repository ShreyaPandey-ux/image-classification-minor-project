import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision


BaseOptions = mp.tasks.BaseOptions
ImageClassifier = mp.tasks.vision.ImageClassifier
ImageClassifierOptions = mp.tasks.vision.ImageClassifierOptions
VisionRunningMode = mp.tasks.vision.RunningMode

def classify_image(filepath="static/uploads/tvs.jpg",model_path = "model.tflite"):
    options = ImageClassifierOptions(
        base_options=BaseOptions(model_asset_path=model_path),
        max_results=5,
        running_mode=VisionRunningMode.IMAGE)

    input_image = mp.Image.create_from_file(filepath)

    with ImageClassifier.create_from_options(options) as classifier:
        # Perform image classification on the provided single image.
        classification_result = classifier.classify(input_image)
        return classification_result.classifications[0].categories
            

if __name__ == '__main__':
    print(classify_image())