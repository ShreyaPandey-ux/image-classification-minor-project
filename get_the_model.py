import kagglehub

# Download latest version
path = kagglehub.model_download("tensorflow/efficientnet/tfLite/lite0-int8")

print("Path to model files:", path)