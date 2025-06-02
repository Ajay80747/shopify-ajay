const options = {
    key: 'YOUR_RAZORPAY_KEY', // Replace with your Razorpay key
    amount: 10000, // Amount in paise (e.g., 10000 = ₹100)
    currency: 'INR',
    name: 'ShopMix',
    description: 'Purchase on ShopMix',
    image: '/static/images/logo.png', // Optional logo
    handler: function (response) {
        alert('Payment Successful!\nPayment ID: ' + response.razorpay_payment_id);
        
        // Optional: Post payment info to server
        fetch('/payment-success', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ payment_id: response.razorpay_payment_id })
        })
        .then(res => res.json())
        .then(data => console.log(data));
    },
    prefill: {
        name: 'Ajay',
        email: 'ajay@example.com',
        contact: '9999999999'
    },
    theme: {
        color: 'red'
    }
};

document.getElementById('pay-btn').onclick = function(e) {
    const rzp = new Razorpay(options);
    rzp.open();
    e.preventDefault();
};
