

    // Show the pop-up
$('#share-button').on('click', function() {
    $('#popup-overlay').show();
    $('#share-popup').show();
});

// Hide the pop-up
$('#popup-overlay').on('click', function() {
    $('#popup-overlay').hide();
    $('#share-popup').hide();
});     



function getCSRFToken() {
        var csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
        return csrfToken;
    }

function uploadFile() {
    var formData = new FormData();
    var file = document.getElementById("id_video_file").files[0];
    formData.append("id_video_file", file);

    var xhr = new XMLHttpRequest();
    
    xhr.open("POST", "", true);
    xhr.setRequestHeader("X-CSRFToken", getCSRFToken());
    xhr.upload.onprogress = function(event) {
        if (event.lengthComputable) {
            var percentComplete = (event.loaded / event.total) * 100;
            var progressBar = document.getElementById("progress");
            var progressContainer = document.getElementById("progress-container");

            progressContainer.style.display = "flex";  // Show progress bar
            progressContainer.style.zIndex = '5'
            progressContainer.style.position = "fixed"
            progressBar.style.width = percentComplete + "%";
            progressBar.innerHTML = Math.round(percentComplete) + "%";
        }
    };

    

    xhr.send(formData);
    document.getElementById("progress-container").style.display = "none"; // Hide progress bar after completion
}
