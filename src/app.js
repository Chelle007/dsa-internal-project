document.getElementById('uploadForm').addEventListener('submit', function (event) {
    event.preventDefault();

    const fileInput = document.getElementById('fileInput');
    const resultText = document.getElementById('resultText');

    if (!fileInput.files.length) {
        alert('Please upload an image.');
        return;
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
            console.log('Parsed JSON data:', data);
            if (data.type) {
                resultText.innerHTML = `<h1>Here are the top 5 links to buy ${data.type}</h1>`;
            }
            if (data.links) {
                createCards(data.links)
            } else if (data.error) {
                resultText.innerHTML = `<p style="color: red;">${data.error}</p>`;
            }
        })
        .catch(error => {
            console.error('Error:', error);
            resultText.innerHTML = `<p style="color: red;">Error uploading file</p>`;
        });
});

function createCards(links) {
    links.forEach(item => {
        const card = document.createElement('div');
        card.className = 'card';

        card.innerHTML = `
            <img src="${item.img_url}" alt="${item.name}">
            <h3>${item.name}</h3>
            <p><strong>Price:</strong> ${item.price}</p>
            <p><strong>Shop:</strong> ${item.shop_name}</p>
            <a href="${item.shop_url}" target="_blank">View Product</a>
        `;

        resultCards.appendChild(card);
    });
}