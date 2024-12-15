let searchingInterval;

document.getElementById('uploadForm').addEventListener('submit', function (event) {
    event.preventDefault();

    const fileInput = document.getElementById('fileInput');
    const preferenceInput = document.getElementById('preferenceInput');
    const resultText = document.getElementById('resultText');
    const container = document.getElementById('container');

    if (!fileInput.files.length) {
        alert('Please upload an image.');
        return;
    }

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);
    formData.append('preferences', preferenceInput.value.trim() || "");

    container.classList.add('show-result');
    startSearchingAnimation(resultText);

    fetch('http://127.0.0.1:5000/upload', {
        method: 'POST',
        body: formData,
    })
        .then(response => {
            clearInterval(searchingInterval);
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            clearInterval(searchingInterval);
            console.log('Parsed JSON data:', data);
            if (data.gpt_response && data.links) {
                setTimeout(() => {
                    typeTextAndCreateCards(`${data.gpt_response}`, resultText, data.links);
                }, 500);
            } else if (data.error) {
                resultText.innerHTML = `<p style="color: red;">${data.error}</p>`;
            }
        })
        .catch(error => {
            clearInterval(searchingInterval);
            console.error('Error:', error);
            resultText.innerHTML = `<p style="color: red;">Error uploading file</p>`;
        });
});

function startSearchingAnimation(element) {
    let dots = 0;
    element.textContent = 'Searching';
    searchingInterval = setInterval(() => {
        dots = (dots + 1) % 4;
        element.textContent = 'Searching' + '.'.repeat(dots);
    }, 500);
}

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
            <div class="card-details">
                <h4>${item.name}</h4>
                <p><strong>Price:</strong> ${item.price}</p>
                <p><strong>Shop:</strong> ${item.shop_name}</p>
            </div>
            <button onclick="window.open('${item.product_url}', '_blank')">
                <i class="fas fa-shopping-cart"></i> View Product
            </button>
        `;

        resultCards.appendChild(card);
    });
}