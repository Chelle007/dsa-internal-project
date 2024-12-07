document.addEventListener('DOMContentLoaded', function () {
    // This code will run only after the DOM is fully loaded

    document.getElementById('uploadForm').addEventListener('submit', function (event) {
        event.preventDefault(); // Prevent the default form submission

        const fileInput = document.getElementById('fileInput');
        const resultDiv = document.getElementById('result');

        if (!fileInput.files.length) {
            alert('Please upload an image.');
            return; // No need to return false, just return
        }

        const formData = new FormData();
        formData.append('file', fileInput.files[0]);

        fetch('http://127.0.0.1:5000/upload', {
            method: 'POST',
            body: formData,
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (data.links) {
                    resultDiv.innerHTML = data.links
                        .map(link => `<a href="${link}" target="_blank">${link}</a>`)
                        .join('');
                } else if (data.error) {
                    resultDiv.innerHTML = `<p style="color: red;">${data.error}</p>`;
                }
            })
            .catch(error => {
                console.error('Error:', error);
                resultDiv.innerHTML = `<p style="color: red;">Error uploading file</p>`;
            });
    });
});