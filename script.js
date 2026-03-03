document.addEventListener("DOMContentLoaded", async () => {

    const form = document.getElementById("anagramForm");
    const input = document.querySelector("input[name='letters']");
    const results = document.getElementById("results");
    const stats = document.getElementById("stats");

    let dictionary = [];

    // Load dictionary once
    const response = await fetch("/static/dictionary.txt");
    const text = await response.text();
    dictionary = text.split(/\s+/);

    function frequency(word) {
        const freq = new Array(26).fill(0);
        word = word.toUpperCase();
        for (let char of word) {
            const index = char.charCodeAt(0) - 65;
            if (index >= 0 && index < 26) {
                freq[index]++;
            }
        }
        return freq;
    }

    function canForm(userFreq, wordFreq) {
        for (let i = 0; i < 26; i++) {
            if (wordFreq[i] > userFreq[i]) return false;
        }
        return true;
    }

    form.addEventListener("submit", (e) => {
        e.preventDefault();

        const letters = input.value.replace(/\s/g, "");
        const userFreq = frequency(letters);

        let matches = [];

        for (let word of dictionary) {
            const wordFreq = frequency(word);
            if (canForm(userFreq, wordFreq)) {
                matches.push(word);
            }
        }

        matches.sort((a, b) => a.length - b.length || a.localeCompare(b));

        results.innerHTML = "";
        matches.forEach(word => {
            const div = document.createElement("div");
            div.className = "anagram-word";
            div.innerHTML = `<a href="#">${word}</a>`;
            results.appendChild(div);
        });

        stats.textContent =
            matches.length + " words found for '" + letters.toUpperCase() + "'";
    });

});