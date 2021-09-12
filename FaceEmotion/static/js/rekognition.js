
// Elements for taking the snapshot
var canvas = document.getElementById('canvas');
var context = canvas.getContext('2d');
var video = document.getElementById('video');

function CallRekognition(imageString){
var data = new FormData()
data.append('byte_image', imageString)
console.log(imageString)
    let result = fetch('/rekognition/', {
	method : 'post',
	headers: {
            'Content-Type': 'multipart/form-data',
        },
    body: data,
	})
	console.log(result)
//    result.then(function(response) {
//      console.log('response', response)
//      console.log('header', response.headers.get('Content-Type'))
//      return response.text()
//    })
}

// Trigger photo take
document.getElementById("snap").addEventListener("click", function() {
	context.drawImage(video, 0, 0, 640, 480);

	// Test
    const canvas = document.createElement("canvas");
    // scale the canvas accordingly
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    // draw the video at that frame
    canvas.getContext('2d')
      .drawImage(video, 0, 0, canvas.width, canvas.height);
    // convert it to a usable data URL
    const dataURL = canvas.toDataURL("image/jpeg");
//    console.log(dataURL)
    // Test
    CallRekognition(dataURL)
});
    // Grab elements, create settings, etc.
var video = document.getElementById('video');

// Get access to the camera!
if(navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    // Not adding `{ audio: true }` since we only want video now
    navigator.mediaDevices.getUserMedia({ video: true }).then(function(stream) {
        //video.src = window.URL.createObjectURL(stream);
        video.srcObject = stream;
        video.play();
    });
}
