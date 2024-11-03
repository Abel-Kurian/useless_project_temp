// Elements
const canvasElement = document.getElementById('overlay');
const canvasCtx = canvasElement.getContext('2d');
const imageUpload = document.getElementById('imageUpload');

// Initialize MediaPipe Face Mesh
const faceMesh = new FaceMesh({
    locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/face_mesh/${file}`,
});
faceMesh.setOptions({
    maxNumFaces: 1,
    minDetectionConfidence: 0.5,
    minTrackingConfidence: 0.5,
});
faceMesh.onResults(onResults);

// Load images for overlay
const mustache = new Image();
mustache.src = 'mustache.png'; // Replace with your image path
const glasses = new Image();
glasses.src = 'glasses.png'; // Replace with your image path

// Load image when selected
imageUpload.addEventListener('change', async (event) => {
    const file = event.target.files[0];
    const img = new Image();
    img.src = URL.createObjectURL(file);
    await img.decode();

    // Set canvas dimensions to match image
    canvasElement.width = img.width;
    canvasElement.height = img.height;

    // Draw image to canvas and pass it to FaceMesh
    canvasCtx.drawImage(img, 0, 0, img.width, img.height);
    faceMesh.send({ image: img });
});

// Draw filters on detected landmarks
function onResults(results) {
    if (!results.multiFaceLandmarks) return;

    // Clear previous drawings
    canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);

    // Redraw the uploaded image
    const img = new Image();
    img.src = canvasElement.toDataURL();
    img.onload = () => canvasCtx.drawImage(img, 0, 0);

    results.multiFaceLandmarks.forEach((landmarks) => {
        // Calculate mustache position
        const noseBottom = landmarks[1];
        const mouthTop = landmarks[13];
        const mustacheWidth = Math.abs(mouthTop.x - noseBottom.x) * canvasElement.width * 2;
        const mustacheHeight = mustacheWidth / 3;
        
        // Calculate glasses position
        const leftEye = landmarks[33];
        const rightEye = landmarks[263];
        const glassesWidth = Math.abs(rightEye.x - leftEye.x) * canvasElement.width * 1.5;
        const glassesHeight = glassesWidth / 3;

        // Draw mustache
        canvasCtx.drawImage(
            mustache,
            (noseBottom.x * canvasElement.width) - mustacheWidth / 2,
            (noseBottom.y * canvasElement.height) + mustacheHeight / 4,
            mustacheWidth,
            mustacheHeight
        );

        // Draw glasses
        canvasCtx.drawImage(
            glasses,
            (leftEye.x * canvasElement.width) - glassesWidth / 4,
            (leftEye.y * canvasElement.height) - glassesHeight / 2,
            glassesWidth,
            glassesHeight
        );
    });
}
