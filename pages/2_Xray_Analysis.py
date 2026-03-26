# Mount drive first
from google.colab import drive
drive.mount('/content/drive')

# Install converter
!pip install tf2onnx onnx

import tf2onnx
import tensorflow as tf
import onnx

# Load your saved model
model = tf.keras.models.load_model('/content/drive/MyDrive/xray_cnn_model.h5')

# Convert to ONNX
input_signature = [tf.TensorSpec([None, 150, 150, 3], tf.float32)]
onnx_model, _ = tf2onnx.convert.from_keras(model, input_signature=input_signature)

# Save ONNX model back to Drive
onnx.save(onnx_model, '/content/drive/MyDrive/xray_model.onnx')
print("Done! Check your Google Drive for xray_model.onnx")
