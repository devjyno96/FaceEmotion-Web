
// Elements for taking the snapshot
var canvas = document.getElementById('canvas');
var context = canvas.getContext('2d');
var video = document.getElementById('video');

// Trigger photo take

function RequestRekognition(){
	context.drawImage(video, 0, 0, 640, 480);
    const canvas = document.createElement("canvas");
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    // draw the video at that frame
    canvas.getContext('2d')
      .drawImage(video, 0, 0, canvas.width, canvas.height);
    canvas.toBlob(function(blob) {
    let data = new FormData()
    data.append('file', blob)
    fetch('/rekognition/', {
      method: 'POST',
      body:data
    })
      .then(response => response.json())
      },'image/png');
}

// 주기적 실행
// 중지를 위해 ID 보관
var request_rekognition_id = null;

// 시계 시작
function StartRekognitionInterval() {
    request_rekognition_id = setInterval(RequestRekognition, 500);
}
// 시계 중지
function StopRekognitionInterval() {
    clearInterval(request_rekognition_id);

}


// 분석 결과 요청 interval 생성
function RequestRekognitionResult(){
    let params = { "user_id": 1};
    let query = Object.keys(params).map(k => encodeURIComponent(k) + '=' + encodeURIComponent(params[k])).join('&');
    let url = '/rekognition/result/duration?' + query;
    fetch(url, {
      method: 'GET',
    }).then((res) => {
        return res.json(); //Promise 반환
    })
    .then((json) => {
        myChart.destroy();
        var ctx = document.getElementById('myChart');
        myChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: json['labels'],
                datasets: [{
                    label: '감정 수치',
                    data: [85.1, 19, 3],
                    backgroundColor: json['backgroundColor'],
                    borderColor:  json['borderColor'],
                    borderWidth: 3,
                }]
            },
            options: {
                responsive: false,
                scales: {
                    y: {
                        max: 100,
                        beginAtZero: true,
                        maintainAspectRatio: false,
                    }
                }
            }
        });

    });

}
//setInterval(RequestRekognitionResult, 500);

document.getElementById("rekognition_start").addEventListener("click", StartRekognitionInterval);
document.getElementById("rekognition_stop").addEventListener("click", StopRekognitionInterval);
document.getElementById("rekognition_result").addEventListener("click", RequestRekognitionResult);



// Get access to the camera!
if(navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    // Not adding `{ audio: true }` since we only want video now
    navigator.mediaDevices.getUserMedia({ video: true }).then(function(stream) {
        video.srcObject = stream;
        video.play();
    });
}


var ctx = document.getElementById('myChart');
var myChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ['Smile', 'Anger', 'Surprised'],
        datasets: [{
            label: '감정 수치',
            data: [85.1, 19, 3],
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
            ],
            borderWidth: 3,
        }]
    },
    options: {
        responsive: false,
        scales: {
            y: {
                max: 100,
                beginAtZero: true,
                maintainAspectRatio: false,
            }
        }
    }
});
console.log(myChart)