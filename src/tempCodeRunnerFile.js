links.forEach(item => {
        const card = document.createElement('div');
        card.className = 'card';

        card.innerHTML = `
            <img src="${item.img_url}" alt="${item.name}">
            <div class="card-details">
                <h3>${item.name}</h3>
                <p><strong>Price:</strong> ${item.price}</p>
                <p><strong>Shop:</strong> ${item.shop_name}</p>
            </div>
            <button onclick="window.open('${item.product_url}', '_blank')">
                <i class="fas fa-shopping-cart"></i> View Product
            </button>
        `;

        resultCards.appendChild(card);
    });