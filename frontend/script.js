// P5.js sketch class (unchanged, except we might add new moods if needed)
class MoodSketch {
    constructor(p) {
        this.p = p;
        this.mood = null;
    }

    setMoodData(mood) {
        this.mood = mood;
        this.p.redraw();
    }

    setup() {
        const canvas = this.p.createCanvas(800, 300);
        canvas.parent('visualization');
        this.p.noLoop();
    }

    draw() {
        this.p.clear();
        if (!this.mood) return;

        switch(this.mood) {
            case 'happy':
                this.drawHappyVisualization();
                break;
            case 'sad':
                this.drawSadVisualization();
                break;
            default:
                this.drawNeutralVisualization();
        }
    }

    drawHappyVisualization() {
        this.p.background(255, 253, 231);
        
        // Sun
        this.p.fill(255, 191, 0);
        this.p.noStroke();
        this.p.circle(700, 100, 80);
        
        // Rays
        this.p.stroke(255, 191, 0);
        this.p.strokeWeight(3);
        for (let i = 0; i < 12; i++) {
            let angle = i * this.p.TWO_PI / 12;
            let x1 = 700 + this.p.cos(angle) * 45;
            let y1 = 100 + this.p.sin(angle) * 45;
            let x2 = 700 + this.p.cos(angle) * 60;
            let y2 = 100 + this.p.sin(angle) * 60;
            this.p.line(x1, y1, x2, y2);
        }
    }

    drawSadVisualization() {
        this.p.background(220, 230, 240);
        
        // Clouds
        this.p.noStroke();
        this.p.fill(169, 169, 169);
        this.p.ellipse(650, 80, 100, 60);
        this.p.ellipse(700, 100, 80, 50);
        this.p.ellipse(750, 90, 90, 55);
        
        // Rain drops
        this.p.stroke(150, 150, 190);
        this.p.strokeWeight(2);
        for (let i = 0; i < 30; i++) {
            let x = this.p.random(600, 800);
            let y = this.p.random(120, 200);
            this.p.line(x, y, x - 5, y + 15);
        }
    }

    drawNeutralVisualization() {
        this.p.background(235, 245, 250);
        
        // Waves
        this.p.noFill();
        this.p.stroke(100, 149, 237);
        this.p.strokeWeight(2);
        for (let i = 0; i < 5; i++) {
            let y = 100 + i * 20;
            this.p.beginShape();
            for (let x = 600; x < 800; x += 10) {
                this.p.vertex(x, y + this.p.sin(x * 0.05 + i) * 10);
            }
            this.p.endShape();
        }
    }
}

let moodSketch = null;

// Show compose form
document.getElementById('composeButton').addEventListener('click', () => {
    const form = document.getElementById('composeForm');
    form.style.display = form.style.display === 'none' ? 'block' : 'none';
});

async function submitJournal() {
    const title = document.getElementById("titleInput").value.trim();
    const location = document.getElementById("locationInput").value.trim();
    const weather = document.getElementById("weatherInput").value.trim();
    const journalText = document.getElementById("journalInput").value.trim();

    if (!journalText) {
        alert("Please enter your journal text.");
        return;
    }

    // Display the submitted journal
    document.getElementById('displayTitle').textContent = title;
    document.getElementById('displayLocation').textContent = location;
    document.getElementById('displayWeather').textContent = weather;
    document.getElementById('displayJournalText').textContent = journalText;
    document.getElementById('journalDisplay').style.display = 'block';

    try {
        const response = await fetch('http://127.0.0.1:5000/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                title: title,
                location: location,
                weather: weather,
                text: journalText
            })
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
    // Update mood visualization
    if (moodSketch) {
        moodSketch.setMoodData(data.mood);
    }

    // Show the output section
    document.getElementById('output').style.display = 'block';

    // Update text content
    document.getElementById('moodDisplay').textContent = `Detected Mood: ${data.mood.charAt(0).toUpperCase() + data.mood.slice(1)}`;
    document.getElementById('personalizedMessage').textContent = data.personalized_message;

    // Support response
    if (data.support_response) {
        document.getElementById('validationMessage').textContent = data.support_response.validation;
        const copingList = document.getElementById('copingStrategies');
        copingList.innerHTML = '';
        data.support_response.coping_strategies.forEach(strategy => {
            const li = document.createElement('li');
            li.textContent = strategy;
            copingList.appendChild(li);
        });
    }

    // Update playlist links
    const musicList = document.getElementById('musicList');
    musicList.innerHTML = '';
    data.music_recommendations.forEach(playlist => {
        const li = document.createElement('li');
        const a = document.createElement('a');
        a.href = playlist.url;
        a.target = '_blank';
        a.textContent = playlist.name;
        a.className = 'playlist-link';
        li.appendChild(a);
        musicList.appendChild(li);
    });
}

// Initialize P5 sketch
new p5((p) => {
    moodSketch = new MoodSketch(p);
    p.setup = () => moodSketch.setup();
    p.draw = () => moodSketch.draw();
}, 'visualization');
