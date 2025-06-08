// // Show loading animation on submit
// function submitURL() {
//     document.getElementById("loading").style.display = "block";
//     setTimeout(() => {
//         document.getElementById("loading").style.display = "none";
//     }, 2000);
// }

// // FAQ Dropdown Functionality
// document.querySelectorAll(".faq-question").forEach(button => {
//     button.addEventListener("click", () => {
//         const answer = button.nextElementSibling;
//         answer.style.display = answer.style.display === "block" ? "none" : "block";
//     });
// });


// gate.js

function showPopup(message) {
    const popup = document.createElement("div");
    popup.className = "popup-alert";
    popup.innerText = message;

    document.body.appendChild(popup);

    setTimeout(() => {
        popup.classList.add("visible");
    }, 10);

    setTimeout(() => {
        popup.classList.remove("visible");
        setTimeout(() => popup.remove(), 300);
    }, 3000);
}

async function submitURL(event) {
    event.preventDefault(); // Prevent form reload

    const urlInput = document.getElementById("response-url");
    const loadingDiv = document.getElementById("loading");

    if (!urlInput.value.trim()) {
        alert("Please enter a valid URL.");
        return;
    }

    loadingDiv.style.display = "block";

    const formData = new FormData();
    formData.append("response_sheet_url", urlInput.value);

    try {
        const response = await fetch("/gatee", {  // Changed endpoint to /gate
            method: "POST",
            body: formData,
        });

        const contentType = response.headers.get("Content-Type");

        if (!response.ok) {
            if (contentType && contentType.includes("application/json")) {
                const errorData = await response.json();
                showPopup(errorData.error || "Something went wrong.");
            } else {
                showPopup("Unexpected server error. Please try again.");
            }
            return;
        }

        const html = await response.text();

        // Replace the current document with the returned HTML
        document.open();
        document.write(html);
        document.close();

    } catch (error) {
        showPopup("An error occurred while submitting. Please try again.");
        console.error("Submission error:", error);
    } finally {
        loadingDiv.style.display = "none";
    }
}

// FAQ Dropdown Functionality
document.querySelectorAll(".faq-question").forEach(button => {
    button.addEventListener("click", () => {
        const answer = button.nextElementSibling;
        answer.style.display = answer.style.display === "block" ? "none" : "block";
    });
});

