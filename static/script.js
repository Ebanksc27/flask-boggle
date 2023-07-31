class BoggleGame {
    constructor(score = 0, timer = 60) {
        this.score = score;
        this.timer = timer;
        this.words = [];
        this.intervalId = null;
    }

    startGame() {
        this.intervalId = setInterval(this.decreaseTimer.bind(this), 1000);
        document.querySelector('#guess-form').addEventListener('submit', this.handleGuess.bind(this));
    }

    async handleGuess(e) {
        e.preventDefault();
        let guess = document.querySelector('#guess-input').value;
        let response = await axios.post('/check-word', {word: guess});
        let message = document.querySelector('#message');
        if (response.data.result === 'ok') {
            this.words.push(guess);  // add word to words list
            this.updateWordsList();  // update HTML
            this.score += guess.length;
            document.querySelector('#score').innerText = `Score: ${this.score}`;
            message.innerText = '';
        } else if (response.data.result === 'not-word') {
            message.innerText = `${guess} is not a valid word.`;
        } else if (response.data.result === 'not-on-board') {
            message.innerText = `${guess} is not on the board.`;
        }
        document.querySelector('#guess-input').value = '';
    }
    
    
    updateWordsList() {
        let wordsList = document.querySelector('#words-list');
        wordsList.innerHTML = '';  // Clear current list
        this.words.forEach(word => {
            let li = document.createElement('li');
            li.classList.add('list-group-item');
            li.innerText = word;
            wordsList.appendChild(li);
        });
    }
    
    

    decreaseTimer() {
        if (this.timer <= 0) {
            clearInterval(this.intervalId);
            this.endGame();
        } else {
            this.timer--;
            document.querySelector('#timer').innerText = `Time: ${this.timer}`;
        }
    }

    async endGame() {
        document.querySelector('#guess-form').remove();
        alert('Game over! Your score is ' + this.score);
        let response = await axios.post('/post-score', {score: this.score});
        if (response.status === 200) {
            let data = response.data;
            document.querySelector('#games-played').innerText = 'Games Played: ' + data.games_played;
            document.querySelector('#high-score').innerText = 'High Score: ' + data.high_score;
        } else {
            console.log('There was an issue posting the score to the server.');
        }
    }
}

// Start the game
let game = new BoggleGame();
game.startGame();





