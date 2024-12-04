document.getElementById('uploadForm').addEventListener('submit', async function (event) {
    event.preventDefault();

    const fileInput = document.getElementById('fileInput');
    const clothingType = document.getElementById('clothingType').value;
    const resultDiv = document.getElementById('result');

    if (!fileInput.files.length || !clothingType) {
        alert('Please upload an image and enter a clothing type.');
        return;
    }

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);
    formData.append('clothingType', clothingType);

    try {
        const response = await fetch('http://127.0.0.1:5000/upload', {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            throw new Error('Failed to fetch');
        }

        const data = await response.json();
        if (data.links) {
            resultDiv.innerHTML = data.links
                .map(link => `<a href="${link}" target="_blank">${link}</a>`)
                .join('');
        } else if (data.error) {
            resultDiv.innerHTML = `<p style="color: red;">${data.error}</p>`;
        }
    } catch (error) {
        console.error(error);
        alert('Error uploading file.');
    }
});
