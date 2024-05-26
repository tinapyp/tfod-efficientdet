from flask import Flask, render_template, request, redirect, url_for
import os
import base64
import cv2
import numpy as np
import tensorflow as tf
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils
from object_detection.builders import model_builder
from object_detection.utils import config_util

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static/uploads/"

PIPELINE_CONFIG = "models/tuned-model/pipeline.config"
CHECKPOINT_PATH = "models/tuned-model/ckpt-3"
LABELMAP = "src/annotations/label_map.pbtxt"

# Load pipeline config and build a detection model
configs = config_util.get_configs_from_pipeline_file(PIPELINE_CONFIG)
detection_model = model_builder.build(model_config=configs["model"], is_training=False)

# Restore checkpoint
ckpt = tf.compat.v2.train.Checkpoint(model=detection_model)
ckpt.restore(CHECKPOINT_PATH).expect_partial()


@tf.function
def detect_fn(image):
    image, shapes = detection_model.preprocess(image)
    prediction_dict = detection_model.predict(image, shapes)
    detections = detection_model.postprocess(prediction_dict, shapes)
    return detections


category_index = label_map_util.create_category_index_from_labelmap(LABELMAP)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return redirect(request.url)
    file = request.files["file"]
    if file.filename == "":
        return redirect(request.url)
    if file:
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(filepath)
        processed_image_path, item_name, item_count = detect_objects(filepath)
        return render_template(
            "result.html",
            filename=processed_image_path,
            item_name=item_name,
            item_count=item_count,
        )


@app.route("/capture", methods=["POST"])
def capture():
    image_data = request.form["image"]
    image_data = base64.b64decode(image_data.split(",")[1])
    raw_image_path = os.path.join(app.config["UPLOAD_FOLDER"], "captured_image.png")
    with open(raw_image_path, "wb") as f:
        f.write(image_data)
    processed_image_path, item_name, item_count = detect_objects(raw_image_path)
    print(processed_image_path)
    return render_template(
        "result.html",
        filename=processed_image_path,
        item_name=item_name,
        item_count=item_count,
    )


def detect_objects(image_path):
    img = cv2.imread(image_path)
    image_np = np.array(img)
    input_tensor = tf.convert_to_tensor(np.expand_dims(image_np, 0), dtype=tf.float32)
    detections = detect_fn(input_tensor)
    num_detections = int(detections.pop("num_detections"))
    detections = {
        key: value[0, :num_detections].numpy() for key, value in detections.items()
    }
    detections["num_detections"] = num_detections
    detections["detection_classes"] = detections["detection_classes"].astype(np.int64)
    label_id_offset = 1
    image_np_with_detections = image_np.copy()
    viz_utils.visualize_boxes_and_labels_on_image_array(
        image_np_with_detections,
        detections["detection_boxes"],
        detections["detection_classes"] + label_id_offset,
        detections["detection_scores"],
        category_index,
        use_normalized_coordinates=True,
        max_boxes_to_draw=5,
        min_score_thresh=0.4,
        agnostic_mode=False,
    )
    processed_image_path = os.path.join(
        app.config["UPLOAD_FOLDER"], "processed_" + os.path.basename(image_path)
    )
    cv2.imwrite(
        processed_image_path, image_np_with_detections
    )  # Save the image with detections
    item_name = (
        "Detected Item"  # Example, extract real item name from detections if needed
    )
    item_count = 1  # Example, update with real item count
    return processed_image_path, item_name, item_count


if __name__ == "__main__":
    app.run(debug=True)
