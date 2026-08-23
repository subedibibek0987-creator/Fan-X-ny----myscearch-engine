async function search() {
  const query = document.getElementById("query").value;

  try {
    const res = await fetch(`/search?q=${encodeURIComponent(query)}`);
    const data = await res.json();

    const resultsDiv = document.getElementById("results");
    resultsDiv.innerHTML = "";

    if (data.RelatedTopics && data.RelatedTopics.length > 0) {
      data.RelatedTopics.forEach(item => {
        if (item.Text && item.FirstURL) {
          const div = document.createElement("div");
          div.className = "result-card";
          div.innerHTML = `
            <h2 class="result-title">
              <a href="${item.FirstURL}" target="_blank">${item.Text}</a>
            </h2>
            <p class="result-snippet">${item.Text}</p>
            <p class="result-link">${item.FirstURL}</p>
          `;
          resultsDiv.appendChild(div);
        }
      });
    } else {
      resultsDiv.innerHTML = "<p>No results found.</p>";
    }
  } catch (error) {
    console.error(error);
    document.getElementById("results").innerHTML = `<p>Error: ${error.message}</p>`;
  }
}
