

function handleSubmit() {
    const inputValue = document.getElementById("inputBox").value;
    fetch("http://localhost:5000/api", { // Update the URL
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ data: inputValue })
    })
    .then(response => response.json())
    .then(result => console.log("Response:", result))
    .catch(error => console.error("Error:", error));
}
