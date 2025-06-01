import cv2
import numpy as np
import json
import matplotlib.pyplot as plt
import os

# === CONFIGURATION ===
input_path = "Countouring_Bldgs/buildingfootprint_trial.png"
output_inverted_path = "Countouring_Bldgs/buildingfootprint_inverted.png"
output_geojson_path = "Countouring_Bldgs/building_contours.geojson"

# === STEP 1: Load grayscale image ===
image = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)
if image is None:
    raise FileNotFoundError(f"Image not found at {input_path}")

# === STEP 2: Invert the image (to make buildings white) ===
inverted = cv2.bitwise_not(image)
cv2.imwrite(output_inverted_path, inverted)

# === STEP 3: Threshold to binary ===
_, thresh = cv2.threshold(inverted, 100, 255, cv2.THRESH_BINARY)  # Lowered threshold

# === STEP 4: Find contours ===
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
print(f"Found {len(contours)} raw contours.")

# === STEP 5: Convert contours to GeoJSON format ===
features = []
for i, cnt in enumerate(contours):
    coords = cnt.squeeze().tolist()
    print(f"Contour {i} has {len(coords)} points.")

    if not coords or isinstance(coords[0], int) or len(coords) < 3:
        continue
    if coords[0] != coords[-1]:  # Ensure polygon is closed
        coords.append(coords[0])
    features.append({
        "type": "Feature",
        "geometry": {
            "type": "Polygon",
            "coordinates": [coords]
        },
        "properties": {}
    })

geojson = {
    "type": "FeatureCollection",
    "features": features
}

# Save GeoJSON
with open(output_geojson_path, "w") as f:
    json.dump(geojson, f, indent=2)

print(f"Saved {len(features)} building footprints to {output_geojson_path}")

# === STEP 6: Preview the contours ===
preview = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
cv2.drawContours(preview, contours, -1, (0, 255, 0), 1)

plt.figure(figsize=(10, 10))
plt.imshow(cv2.cvtColor(preview, cv2.COLOR_BGR2RGB))
plt.title(f"Detected {len(features)} Contours")
plt.axis("off")
plt.show(block=False)
plt.pause(3)
plt.close()
