function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    const container = document.querySelector('.container');

    if (sidebar.style.left === "-250px") {
        sidebar.style.left = "0";
        container.style.marginLeft = "250px";
    } else {
        sidebar.style.left = "-250px";
        container.style.marginLeft = "0";
    }
}



function changeTheme() {
    const theme = document.getElementById('theme-selector').value;
    document.body.className = `theme-${theme}`;
}

function toggleVisibility(id) {
            var element = document.getElementById(id);
            if (element.style.display === "none") {
                element.style.display = "block";
            } else {
                element.style.display = "none";
            }
        }

function showLink(linkId) {
            const link = document.getElementById(linkId);
            if (link.style.display === "none") {
                link.style.display = "block";
            } else {
                link.style.display = "none";
            }
        }

document.addEventListener('DOMContentLoaded', function() {
    // Cargar Noticias de Internet usando la API
    const apiKey = '8860e3f3753f413aa9833e9ec1862357';
    const url = `https://newsapi.org/v2/top-headlines?country=us&category=technology&apiKey=${apiKey}`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            const newsContainer = document.getElementById('internet-news');
            if (data.articles && data.articles.length > 0) {
                data.articles.forEach(article => {
                    const newsItem = document.createElement('div');
                    newsItem.classList.add('news-item');
                    newsItem.innerHTML = `
                        <img src="${article.urlToImage}" alt="${article.title}">
                        <h4>${article.title}</h4>
                        <p>${article.description}</p>
                        <a href="${article.url}" target="_blank">Leer más</a>
                    `;
                    newsContainer.appendChild(newsItem);
                });
            } else {
                newsContainer.innerHTML = "<p>No hay noticias disponibles en este momento.</p>";
            }
        })
        .catch(error => {
            console.error("Error al cargar las noticias:", error);
            const newsContainer = document.getElementById('internet-news');
            newsContainer.innerHTML = "<p>Error al cargar noticias. Inténtalo de nuevo más tarde.</p>";
        });

});

async function sendMessage() {
    const message = document.getElementById('chat-message').value;
    const chatBox = document.getElementById('chat-box');

    if (message.trim() !== '') {
        chatBox.innerHTML += `<p class="user-message">${message}</p>`;
        document.getElementById('chat-message').value = '';  // Limpiar campo

        try {
            // Llamada a la API del chatbot
            const response = await fetch("/chatbot", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: message })
            });

            const data = await response.json();
            chatBox.innerHTML += `<p class="bot-response">${data.response}</p>`;
            chatBox.scrollTop = chatBox.scrollHeight;  // Desplazar hacia abajo
        } catch (error) {
            console.error("Error al enviar mensaje:", error);
            chatBox.innerHTML += `<p class="bot-response error">Error al enviar mensaje. Inténtalo de nuevo.</p>`;
        }
    }
}

