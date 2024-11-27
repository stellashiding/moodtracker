async function submitReflection() {
    const userInput = document.getElementById("userInput").value.trim();
    if (!userInput) {
        alert("Please enter your thoughts.");
        return;
    }
    
    // Send input to backend for analysis
    try {
        const response = await fetch('http://127.0.0.1:5000/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: userInput })
        });
        
        if (!response.ok) {
            throw new Error("Network response was not ok");
        }
        
        const data = await response.json();
        displayResults(data);
    } catch (error) {
        console.error("Error:", error);
        alert("An error occurred while processing your input. Please try again.");
    }
}

function displayResults(data) {
    const moodDisplay = document.getElementById("moodDisplay");
    const personalizedMessage = document.getElementById("personalizedMessage");
    const musicList = document.getElementById("musicList");
    
    // Display Mood
    const moodCapitalized = capitalizeFirstLetter(data.mood);
    moodDisplay.innerText = `Detected Mood: ${moodCapitalized}`;
    
    // Display Personalized Message
    personalizedMessage.innerText = data.personalized_message;
    
    // Display Music Recommendations
    musicList.innerHTML = "";
    data.music_recommendations.forEach(playlist => {
        const li = document.createElement("li");
        const a = document.createElement("a");
        a.href = playlist.url;
        a.target = "_blank";
        a.innerText = playlist.name;
        li.appendChild(a);
        musicList.appendChild(li);
    });
    
    // Trigger P5.js visualization
    new p5((p) => sketch(p, data.mood));
}

function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}

// P5.js Sketch Function
function sketch(p, mood) {
    p.setup = function() {
        p.createCanvas(400, 200);
    };

    p.draw = function() {
        p.clear();
        if (mood === "happy") {
            p.background(255, 223, 0); // Bright yellow
            p.fill(255, 87, 34); // Orange
            p.ellipse(p.width / 2, p.height / 2, 100, 100);
        } else if (mood === "sad") {
            p.background(70, 130, 180); // Steel blue
            p.fill(25, 25, 112); // Midnight blue
            p.rect(p.width / 2 - 50, p.height / 2 - 25, 100, 50);
        } else {
            p.background(200, 200, 200); // Light gray
            p.fill(100, 100, 100); // Dark gray
            p.triangle(p.width / 2, p.height / 2 - 50, p.width / 2 - 50, p.height / 2 + 50, p.width / 2 + 50, p.height / 2 + 50);
        }
    };
}
