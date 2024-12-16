function loadCards() {
    fetch('/api/cards')
        .then(response => response.json())
        .then(data => {
            const gallery = document.getElementById('cardGallery');
            gallery.innerHTML = '';
            data.forEach(card => {
                gallery.innerHTML += `
                    <div>
                        <img src="${card.image}" width="150" />
                        <h3>${card.name}</h3>
                        <p>Price: ${card.price}</p>
                        <button onclick="addToWishlist('${card.name}', '${card.price}')">Add to Wishlist</button>
                    </div>`;
            });
        });
}

function generateCard(type) {
    fetch(`/api/generate-${type}-card`, { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            document.getElementById(`${type}CardImage`).src = data.url;
        });
}

function addToWishlist(name, price) {
    fetch('/api/add-to-wishlist', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ card: { name, price } })
    }).then(() => loadWishlist());
}

function transcribeAudio() {
    const audioFile = document.getElementById("audioUpload").files[0];
    const formData = new FormData();
    formData.append("audio", audioFile);

    fetch('/api/transcribe-audio', { method: 'POST', body: formData })
        .then(response => response.json())
        .then(data => alert(`Transcription: ${data.transcription}`));
}

function analyzeImage() {
    const imageFile = document.getElementById("imageUpload").files[0];
    const formData = new FormData();
    formData.append("image", imageFile);

    fetch('/api/analyze-image', { method: 'POST', body: formData })
        .then(response => response.json())
        .then(data => alert(`Analysis Result: ${data.analysis}`));
}

function askChatbot() {
    const userMessage = document.getElementById('userMessage').value;
    fetch('/api/ask-chatbot', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userMessage })
    })
        .then(response => response.json())
        .then(data => alert(`Chatbot: ${data.reply}`));
}

window.onload = () => {
    loadCards();
    loadWishlist();
};
