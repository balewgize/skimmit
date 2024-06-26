const articleForm = document.getElementById('article-form');
const videoForm = document.getElementById('video-form');
const articleInput = document.querySelector('input[name="article"]');
const videoInput = document.querySelector('input[name="video"]');

const resultDiv = document.getElementById('result');
const loadingDiv = document.getElementById('loading');
const noSummaryMessage = "Oops! Something went wrong. Please try again (or use a different link)."

// handle theme change
const toggleTheme = document.getElementById('toggle-theme');

toggleTheme.addEventListener('click', () => {
    const currentTheme = localStorage.getItem('skTheme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

    document.documentElement.setAttribute('data-bs-theme', newTheme);
    localStorage.setItem('skTheme', newTheme);
});

document.addEventListener('DOMContentLoaded', () => {
    const savedTheme = localStorage.getItem('skTheme') || 'light'; // Default to light theme
    document.documentElement.setAttribute('data-bs-theme', savedTheme);
});


const fetchSummary = (url, source) => {
    showLoadingText();

    fetch('/summarize', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            url: url, source: source,
        })
    })
        .then(response => {
            if (response.ok) {
                return response.json();
            }
            throw new Error('Network response was not ok.');
        })
        .then(data => {
            // console.log(data);
            showResult(data, url);
        })
        .catch(error => {
            // console.error('There was a problem with your fetch operation:', error);
            resultDiv.innerHTML = noSummaryMessage;
            loadingDiv.classList.add('d-none');
        });
}

const showResult = (data, url) => {
    if (!data) {
        resultDiv.innerHTML = noSummaryMessage;
        articleInput.value = '';
        loadingDiv.classList.add('d-none');
        return;
    }
    const { title, sentences } = data;

    resultDiv.innerHTML = `
        <h6 class="mb-3"><span class="text-muted">Title:</span> ${title}</h6>
        <ul class="summary">
            ${sentences.map(sentence => `<li>${sentence}</li>`).join('')}
        </ul>
        <a href="${url}" target="_blank" class="btn btn-secondary mt-3">View Original</a>
    `;
    articleInput.value = '';
    videoInput.value = '';
    loadingDiv.classList.add('d-none');
};

const showLoadingText = () => {
    loadingDiv.classList.remove('d-none');
    const loadingText = document.getElementById('loading-text');
    const loadingMessages = [
        "Fetching details... 📡",
        "Analyzing content... 🔍",
        "Generating your summary... ✍️",
        "Almost there! Finalizing... 🚀",

    ];
    loadingMessages.forEach((message, index) => {
        setTimeout(() => {
            loadingText.textContent = message;
        }, index * 1250);
    });
};


articleForm.addEventListener('submit', (event) => {
    event.preventDefault();

    resultDiv.innerHTML = '';
    const articleUrl = articleInput.value;
    fetchSummary(articleUrl, "article");
});

videoForm.addEventListener('submit', (event) => {
    event.preventDefault();

    resultDiv.innerHTML = '';
    const videoUrl = videoInput.value;
    // Regular expression to validate YouTube URL (standard and shortened)
    const youtubeRegex = /^(https?:\/\/)?(www\.)?(youtube\.com\/watch\?v=|youtu\.be\/)[a-zA-Z0-9_-]{11}.*/;

    if (!youtubeRegex.test(videoUrl)) {
        resultDiv.innerHTML = 'Please enter a valid YouTube URL.';
        return;
    }

    fetchSummary(videoUrl, "video");
});
