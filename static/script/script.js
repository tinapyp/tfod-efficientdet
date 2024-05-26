function startCamera() {
  const video = document.getElementById("video");
  const camera = document.getElementById("camera");
  camera.style.display = "block";
  const constraints = {
    video: true,
  };

  navigator.mediaDevices
    .getUserMedia(constraints)
    .then((stream) => {
      video.srcObject = stream;
    })
    .catch((err) => {
      console.error("Error accessing camera: ", err);
    });
}

function captureImage() {
  const video = document.getElementById("video");
  const canvas = document.getElementById("canvas");
  const context = canvas.getContext("2d");
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  context.drawImage(video, 0, 0, canvas.width, canvas.height);
  const imageData = canvas.toDataURL("image/png");
  document.getElementById("imageData").value = imageData;
  document.getElementById("captureForm").style.display = "block";
}
