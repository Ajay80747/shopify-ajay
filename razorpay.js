const options = {
    key: 'YOUR_RAZORPAY_KEY',
    amount: 10000,
    currency: 'INR',
    name: 'ShopMix',
    description: 'Test Transaction',
    handler: function (response){
        alert('Payment Successful!');
    }
};
document.getElementById('pay-btn').onclick = function(e){
    const rzp = new Razorpay(options);
    rzp.open();
    e.preventDefault();
}