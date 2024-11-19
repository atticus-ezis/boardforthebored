// document.addEventListener("DOMContentLoaded", function () {
//   let typingTimer;
//   const debounceDelay = 300; // Delay to prevent too many requests

//   document.getElementById("city").addEventListener("input", function () {
//     clearTimeout(typingTimer); // Clear previous timer
//     const query = this.value;

//     // Debounce: Only trigger the fetch if the user stops typing for a brief moment
//     typingTimer = setTimeout(() => {
//       if (query.length > 1) {
//         // Only search if more than 1 character
//         fetch(`http://127.0.0.1:8000/city-state-autocomplete/?city=${query}`)
//           .then((response) => response.json())
//           .then((data) => {
//             const resultsList = document.getElementById("autocomplete-results");
//             resultsList.innerHTML = ""; // Clear previous results

//             // Display each result as an option
//             data.results.forEach((result) => {
//               const li = document.createElement("li");
//               li.classList.add("list-group-item");
//               li.textContent = result;
//               li.onclick = function () {
//                 document.getElementById("city").value = result;
//                 resultsList.innerHTML = ""; // Clear the list after selection
//               };
//               resultsList.appendChild(li);
//             });
//           })
//           .catch((error) =>
//             console.error("Error fetching autocomplete results:", error)
//           );
//       }
//     }, debounceDelay); // Delay fetch by debounce delay time
//   });
// });
