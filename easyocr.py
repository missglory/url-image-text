import easyocr
import supervision as sv
import cv2
import numpy as np
import os
import sys

# Initialize EasyOCR reader (English language, CPU)
reader = easyocr.Reader(['en'], gpu=False, model_storage_directory='/path/to/directory')

def apply_ocr_pipeline(image_path):
    # Perform text detection on the image
    result = reader.readtext(image_path)

    # Load image using OpenCV
    image = cv2.imread(image_path)

    # Prepare lists for bounding boxes, confidences, class IDs, and labels
    xyxy, confidences, class_ids, label = [], [], [], []

    # Extract data from OCR result
    for detection in result:
        bbox, text, confidence = detection[0], detection[1], detection[2]
       
        # Convert bounding box format
        x_min = int(min([point[0] for point in bbox]))
        y_min = int(min([point[1] for point in bbox]))
        x_max = int(max([point[0] for point in bbox]))
        y_max = int(max([point[1] for point in bbox]))
       
        # Append data to lists
        xyxy.append([x_min, y_min, x_max, y_max])
        label.append(text)
        confidences.append(confidence)
        class_ids.append(0)  

    # Convert to NumPy arrays
    detections = sv.Detections(
        xyxy=np.array(xyxy),
        confidence=np.array(confidences),
        class_id=np.array(class_ids)
    )

    # Annotate image with bounding boxes and labels
    box_annotator = sv.BoxAnnotator()
    label_annotator = sv.LabelAnnotator()

    annotated_image = box_annotator.annotate(scene=image, detections=detections)
    annotated_image = label_annotator.annotate(scene=annotated_image, detections=detections, labels=label)

    # Display and save the annotated image
    sv.plot_image(image=annotated_image)
    filename, file_extension = os.path.splitext(image_path)
    cv2.imwrite(f"{filename}_output{file_extension}", annotated_image)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python easyocr.py <source_folder>")
        sys.exit(1)

    source_folder = sys.argv[1]

    for filename in os.listdir(source_folder):
        if filename.endswith(".jpg"):
            image_path = os.path.join(source_folder, filename)
            apply_ocr_pipeline(image_path)
