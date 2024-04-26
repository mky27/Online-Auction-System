// Periodically check if auctions have ended
setInterval(function() {
    fetch("{% url 'update_auction_status' %}")
    .then(response => {
        if (response.ok) {
            // Reload the page if the status update was successful
            window.location.reload();
        } else {
            console.error("Failed to update auction status");
        }
    })
    .catch(error => console.error("Error:", error));
}, 60000); // Check every minute
