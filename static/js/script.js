document.addEventListener("DOMContentLoaded", function () {
  let typingTimer;
  const debounceDelay = 300; // Delay to prevent too many requests
  const resultsList = document.getElementById("autocomplete-results");
  document.getElementById("city").addEventListener("input", function () {
    clearTimeout(typingTimer); // Clear previous timer
    const query = this.value;

    // Debounce: Only trigger the fetch if the user stops typing for a brief moment
    typingTimer = setTimeout(() => {
      if (query.length > 1) {
        // Only search if more than 1 character
        fetch(`/autocomplete/?city=${encodeURIComponent(query)}`)
          .then((response) => response.json())
          .then((data) => {
            resultsList.innerHTML = ""; // Clear previous results

            if (data) {
              // Display each result as an option
              data.forEach((result) => {
                const li = document.createElement("li");
                li.classList.add("list-group-item");
                li.textContent = `${result.city}, ${result.state}`;
                li.onclick = function () {
                  document.getElementById(
                    "city"
                  ).value = `${result.city}, ${result.state}`;
                  resultsList.innerHTML = ""; // Clear the list after selection
                  // add a form submit after selection?
                };
                resultsList.appendChild(li);
              });
            }
          })
          .catch((error) => {
            console.error("Error fetching autocomplete results:", error);
          });
      } else {
        resultsList.innerHTML = ""; // Clear previous results
      }
    }, debounceDelay); // Delay fetch by debounce delay time
  });
});

function updateInput() {
  const dropdown = document.getElementById("dropdown_selection");
  const selection = dropdown.value;
  const venue_input = document.getElementById("venue_name_input");
  venue_input.value = selection;
}
