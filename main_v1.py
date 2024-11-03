import  cv2
import mediapipe as mp
import os

# Suppress MediaPipe logging messages
os.environ['GLOG_minloglevel'] = '2'

# main.py
#import runpy
#runpy.run_path("AI_Text_to_Image.py")  # runs script.py as a module

# Load the input image and accessory images (ensure they have transparency)
image_path = "face_image.jpg"  # Replace with your input image path
image = cv2.imread(image_path)
hat = cv2.imread("hat.png", cv2.IMREAD_UNCHANGED)          # Hat with transparency
glasses = cv2.imread("glasses.png", cv2.IMREAD_UNCHANGED)  # Glasses with transparency
mustache = cv2.imread("mustache.png", cv2.IMREAD_UNCHANGED)  # Mustache with transparency

# Get image dimensions
image_height, image_width = image.shape[:2]

# Initialize MediaPipe Face Mesh with image dimensions
mp_face_mesh = mp.solutions.face_mesh
with mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, refine_landmarks=True) as face_mesh:
    # Convert the image to RGB and process it to get facial landmarks
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_image)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            # Position the hat
            forehead_top = (int(face_landmarks.landmark[10].x * image_width), int(face_landmarks.landmark[10].y * image_height))
            chin = (int(face_landmarks.landmark[152].x * image_width), int(face_landmarks.landmark[152].y * image_height))

            # Calculate hat dimensions and position
            hat_width = int((chin[1] - forehead_top[1]) * 1.5)
            hat_height = int(hat.shape[0] * (hat_width / hat.shape[1]))
            resized_hat = cv2.resize(hat, (hat_width, hat_height))
            y_offset_hat = forehead_top[1] - hat_height
            x_offset_hat = forehead_top[0] - hat_width // 2

            # Overlay hat with transparency
            for i in range(3):
                image[y_offset_hat:y_offset_hat + hat_height, x_offset_hat:x_offset_hat + hat_width, i] = \
                    resized_hat[:, :, i] * (resized_hat[:, :, 3] / 255.0) + \
                    image[y_offset_hat:y_offset_hat + hat_height, x_offset_hat:x_offset_hat + hat_width, i] * \
                    (1 - resized_hat[:, :, 3] / 255.0)

            # Position the glasses
            left_eye = (int(face_landmarks.landmark[33].x * image_width), int(face_landmarks.landmark[33].y * image_height))
            right_eye = (int(face_landmarks.landmark[263].x * image_width), int(face_landmarks.landmark[263].y * image_height))

            # Calculate glasses dimensions and position
            glasses_width = right_eye[0] - left_eye[0]
            glasses_height = int(glasses.shape[0] * (glasses_width / glasses.shape[1]))
            resized_glasses = cv2.resize(glasses, (glasses_width, glasses_height))
            y_offset_glasses = left_eye[1] - glasses_height // 2
            x_offset_glasses = left_eye[0] - glasses_width // 4

            # Overlay glasses with transparency
            for i in range(3):
                image[y_offset_glasses:y_offset_glasses + glasses_height, x_offset_glasses:x_offset_glasses + glasses_width, i] = \
                    resized_glasses[:, :, i] * (resized_glasses[:, :, 3] / 255.0) + \
                    image[y_offset_glasses:y_offset_glasses + glasses_height, x_offset_glasses:x_offset_glasses + glasses_width, i] * \
                    (1 - resized_glasses[:, :, 3] / 255.0)

            # Position the mustache
            nose_tip = (int(face_landmarks.landmark[1].x * image_width), int(face_landmarks.landmark[1].y * image_height))
            upper_lip = (int(face_landmarks.landmark[13].x * image_width), int(face_landmarks.landmark[13].y * image_height))

            # Calculate mustache dimensions and position
            mustache_width = int(glasses_width * 0.7)
            mustache_height = int(mustache.shape[0] * (mustache_width / mustache.shape[1]))
            resized_mustache = cv2.resize(mustache, (mustache_width, mustache_height))
            y_offset_mustache = upper_lip[1] - mustache_height // 2
            x_offset_mustache = nose_tip[0] - mustache_width // 2

            # Overlay mustache with transparency
            for i in range(3):
                image[y_offset_mustache:y_offset_mustache + mustache_height, x_offset_mustache:x_offset_mustache + mustache_width, i] = \
                    resized_mustache[:, :, i] * (resized_mustache[:, :, 3] / 255.0) + \
                    image[y_offset_mustache:y_offset_mustache + mustache_height, x_offset_mustache:x_offset_mustache + mustache_width, i] * \
                    (1 - resized_mustache[:, :, 3] / 255.0)

    # Save the final image as output.png
    cv2.imwrite("output.png", image)
    cv2.imshow("Final Output", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
