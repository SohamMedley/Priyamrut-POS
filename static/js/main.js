document.addEventListener('DOMContentLoaded', function() {
    // CART SETUP
    const cart = [];
    let selectedPaymentMethod = null; // track user-chosen payment method
    
    // If these exist, we are on the main menu page
    const foodCards = document.querySelectorAll('.food-card');
    const cartItemsContainer = document.getElementById('cart-items');
    const subtotalElement = document.getElementById('subtotal');
    const taxElement = document.getElementById('tax');
    const totalElement = document.getElementById('total');
    const placeOrderBtn = document.querySelector('.place-order-btn');

    // 1) DINING MODE TOGGLE
    const allModeContainers = document.querySelectorAll('.dining-mode, .cart-dining-mode');
    allModeContainers.forEach(container => {
        const modeBtns = container.querySelectorAll('.mode-btn');
        modeBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                modeBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
            });
        });
    });

    // 2) PAYMENT METHOD SELECTION
    const paymentButtons = document.querySelectorAll('.payment-methods .payment-btn');
    paymentButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            // remove 'active' from all
            paymentButtons.forEach(b => b.classList.remove('active'));
            // add 'active' to clicked
            btn.classList.add('active');
            
            const text = btn.querySelector('span').textContent.toLowerCase();
            if (text.includes('cash')) {
                selectedPaymentMethod = 'cash';
            } else if (text.includes('credit')) {
                selectedPaymentMethod = 'card';
            } else if (text.includes('qr')) {
                selectedPaymentMethod = 'qr';
            }
        });
    });

    // If we are NOT on the main menu page (no cart elements), stop here
    if (!foodCards.length || !cartItemsContainer || !placeOrderBtn) {
        return;
    }

    // 3) ATTACH QTY +/-
    foodCards.forEach(card => {
        const plusBtn = card.querySelector('.plus');
        const minusBtn = card.querySelector('.minus');
        const qtyValue = card.querySelector('.qty-value');
        
        const id = card.dataset.id;
        const title = card.dataset.title;
        const price = parseFloat(card.dataset.price);
        const type = card.dataset.type;
        const image = card.querySelector('img').src;
        
        plusBtn.addEventListener('click', () => {
            let qty = parseInt(qtyValue.textContent);
            qty++;
            qtyValue.textContent = qty;
            
            const existingItem = cart.find(item => item.id === id);
            if (existingItem) {
                existingItem.quantity = qty;
            } else {
                cart.push({ id, title, price, type, image, quantity: qty });
            }
            updateCart();
        });
        
        minusBtn.addEventListener('click', () => {
            let qty = parseInt(qtyValue.textContent);
            if (qty > 0) {
                qty--;
                qtyValue.textContent = qty;
                const existingIndex = cart.findIndex(item => item.id === id);
                if (existingIndex !== -1) {
                    if (qty === 0) {
                        cart.splice(existingIndex, 1);
                    } else {
                        cart[existingIndex].quantity = qty;
                    }
                    updateCart();
                }
            }
        });
    });

    // 4) UPDATE CART
    function updateCart() {
        cartItemsContainer.innerHTML = '';
        let subtotal = 0;
        
        cart.forEach(item => {
            subtotal += item.price * item.quantity;
            const cartItem = document.createElement('div');
            cartItem.className = 'cart-item';
            cartItem.innerHTML = `
                <div class="cart-item-image">
                    <img src="${item.image}" alt="${item.title}">
                </div>
                <div class="cart-item-details">
                    <h4 class="cart-item-title">${item.title}</h4>
                    <div class="cart-item-meta">
                        <span class="cart-item-price">$${item.price.toFixed(2)}</span>
                        <span class="cart-item-quantity">${item.quantity}x</span>
                    </div>
                </div>
            `;
            cartItemsContainer.appendChild(cartItem);
        });
        
        const tax = subtotal * 0.05;
        const total = subtotal + tax;
        subtotalElement.textContent = `$${subtotal.toFixed(2)}`;
        taxElement.textContent = `$${tax.toFixed(2)}`;
        totalElement.textContent = `$${total.toFixed(2)}`;
    }

    // 5) PLACE ORDER
    placeOrderBtn.addEventListener('click', () => {
        if (cart.length === 0) {
            alert('Please add items to your cart before placing an order.');
            return;
        }
        if (!selectedPaymentMethod) {
            alert('Please select a payment method before placing an order.');
            return;
        }
        placeOrderBtn.disabled = true;
        
        const orderData = {
            table: 'Table 4',
            customer: 'Floyd Miles',
            items: cart,
            subtotal: parseFloat(subtotalElement.textContent.replace('$', '')),
            tax: parseFloat(taxElement.textContent.replace('$', '')),
            total: parseFloat(totalElement.textContent.replace('$', '')),
            paymentMethod: selectedPaymentMethod
        };
        
        fetch('/api/place-order', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(orderData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Order placed successfully!');
                // reset cart
                cart.length = 0;
                document.querySelectorAll('.qty-value').forEach(el => { el.textContent = '0'; });
                updateCart();
                // reset payment method
                paymentButtons.forEach(b => b.classList.remove('active'));
                selectedPaymentMethod = null;
            } else {
                alert('Failed to place order. Please try again.');
            }
            placeOrderBtn.disabled = false;
        })
        .catch(error => {
            console.error('Error placing order:', error);
            alert('An error occurred while placing your order. Please try again.');
            placeOrderBtn.disabled = false;
        });
    });

    // 6) CATEGORY FILTERING
    const categoryItems = document.querySelectorAll('.category-item');
    categoryItems.forEach(item => {
        item.addEventListener('click', () => {
            categoryItems.forEach(cat => cat.classList.remove('active'));
            item.classList.add('active');
            
            const selectedCategory = item.querySelector('.category-name').textContent.trim();
            foodCards.forEach(card => {
                const cardCategory = card.dataset.category.trim();
                if (selectedCategory === 'All' || cardCategory === selectedCategory) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });
});
