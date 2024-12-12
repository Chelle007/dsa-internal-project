document.getElementById('uploadForm').addEventListener('submit', function (event) {
    event.preventDefault();

    const fileInput = document.getElementById('fileInput');
    const resultText = document.getElementById('resultText');
    const container = document.getElementById('container');

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
            if (data.type && data.links) {
                setTimeout(() => {
                    typeTextAndCreateCards(`Here are the top 5 most popular ${data.type}:`, resultText, data.links);
                }, 500);
                container.classList.add('show-result');
            } else if (data.error) {
                resultText.innerHTML = `<p style="color: red;">${data.error}</p>`;
                container.classList.add('show-result')
            }
        })
        .catch(error => {
            console.error('Error:', error);
            resultText.innerHTML = `<p style="color: red;">Error uploading file</p>`;
            container.classList.add('show-result');
        });
});

function typeTextAndCreateCards(text, element, links) {
    typeText(text, element);
    setTimeout(() => { createCards(links) }, 1000);
}

function typeText(text, element) {
    element.textContent = ''
    let i = 0;
    let speed = 40;

    function typeWriter() {
        if (i < text.length) {
            element.textContent += text.charAt(i);
            i++;
            setTimeout(typeWriter, speed);
        }
    }

    typeWriter();
}

function createCards(links) {
    resultCards.innerHTML = '';

    links.forEach(item => {
        const card = document.createElement('div');
        card.className = 'card';

        card.innerHTML = `
            <img src="${item.img_url}" alt="${item.name}">
            <h3>${item.name}</h3>
            <p><strong>Price:</strong> ${item.price}</p>
            <p><strong>Shop:</strong> ${item.shop_name}</p>
            <button onclick="window.open('${item.shop_url}', '_blank')">
                <i class="fas fa-shopping-cart"></i> View Product
            </button>
        `;

        resultCards.appendChild(card);
    });
}