document
  .getElementById("fileInput")
  .addEventListener("change", function (event) {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = function (e) {
        const img = document.createElement("img");
        img.src = e.target.result;
        img.classList.add("img-thumbnail", "mt-3");
        img.style.maxWidth = "100%";
        document.getElementById("result").innerHTML = "";
        document.getElementById("result").appendChild(img);
      };
      reader.readAsDataURL(file);
    }
  });

function startCamera() {
  document.getElementById("result").style.display = "none";
  document.getElementById("bottom-buttons").style.display = "none";
  document.getElementById("camera").style.display = "flex";
  document.getElementById("preview").style.display = "none";
  navigator.mediaDevices.getUserMedia({ video: true }).then((stream) => {
    document.getElementById("video").srcObject = stream;
  });
}

function captureImage() {
  const canvas = document.getElementById("canvas");
  const video = document.getElementById("video");
  const context = canvas.getContext("2d");
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  context.drawImage(video, 0, 0, canvas.width, canvas.height);
  const imageData = canvas.toDataURL("image/png");
  document.getElementById("previewImage").src = imageData;
  document.getElementById("preview").style.display = "block";
  document.getElementById("camera").style.display = "none";
}

function retakeImage() {
  document.getElementById("preview").style.display = "none";
  document.getElementById("camera").style.display = "flex";
}

function submitImage() {
  const imageData = document.getElementById("previewImage").src;
  document.getElementById("imageData").value = imageData;
  document.getElementById("captureForm").style.display = "block";
  document.getElementById("captureForm").submit();
}
