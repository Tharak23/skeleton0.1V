import json

def generate_game_code(game_logic):
    """
    Generate Phaser.js game code from game logic JSON
    """
    game_type = game_logic.get("gameType", "continuous")
    
    # Select the appropriate template based on game type
    if game_type == "turnBased" and game_logic.get("name") == "Tic Tac Toe":
        return _generate_tic_tac_toe_code(game_logic)
    elif game_type == "continuous" and "Snake" in game_logic.get("name", ""):
        return _generate_snake_code(game_logic)
    elif game_type == "realtime" and "Pong" in game_logic.get("name", ""):
        return _generate_pong_code(game_logic)
    elif game_type == "continuous" and "Breakout" in game_logic.get("name", ""):
        return _generate_breakout_code(game_logic)
    else:
        # Default to a simple collector game
        return _generate_collector_code(game_logic)

def _generate_tic_tac_toe_code(game_logic):
    """Generate Phaser.js code for Tic Tac Toe game"""
    return """
const config = {
    type: Phaser.AUTO,
    width: 600,
    height: 600,
    backgroundColor: '#f8f8f8',
    scene: {
        preload: preload,
        create: create
    }
};

const gameState = {
    board: [
        ['', '', ''],
        ['', '', ''],
        ['', '', '']
    ],
    currentPlayer: 'X',
    gameOver: false,
    winningLine: null,
    cellSize: 150,
    gridOffset: 120
};

const game = new Phaser.Game(config);

function preload() {
    // Load assets if needed
}

function create() {
    const self = this;
    
    // Create game title
    this.add.text(300, 50, 'Tic Tac Toe', { fontSize: '40px', fontWeight: 'bold', fill: '#333' }).setOrigin(0.5);
    
    // Draw grid with better styling
    const graphics = this.add.graphics();
    
    // Background for the grid
    graphics.fillStyle(0xffffff, 1);
    graphics.fillRoundedRect(105, 105, 390, 390, 10);
    
    // Grid lines
    graphics.lineStyle(3, 0x333333, 1);
    
    // Vertical lines
    graphics.beginPath();
    graphics.moveTo(255, 120);
    graphics.lineTo(255, 480);
    graphics.closePath();
    graphics.strokePath();
    
    graphics.beginPath();
    graphics.moveTo(345, 120);
    graphics.lineTo(345, 480);
    graphics.closePath();
    graphics.strokePath();
    
    // Horizontal lines
    graphics.beginPath();
    graphics.moveTo(120, 255);
    graphics.lineTo(480, 255);
    graphics.closePath();
    graphics.strokePath();
    
    graphics.beginPath();
    graphics.moveTo(120, 345);
    graphics.lineTo(480, 345);
    graphics.closePath();
    graphics.strokePath();
    
    // Player turn text
    gameState.turnText = this.add.text(300, 520, 'Player X turn', { fontSize: '28px', fill: '#333' }).setOrigin(0.5);
    
    // Create clickable cells
    for (let row = 0; row < 3; row++) {
        for (let col = 0; col < 3; col++) {
            const cellX = gameState.gridOffset + col * gameState.cellSize + gameState.cellSize/2;
            const cellY = gameState.gridOffset + row * gameState.cellSize + gameState.cellSize/2;
            
            const cell = this.add.rectangle(cellX, cellY, gameState.cellSize - 10, gameState.cellSize - 10, 0xffffff, 0);
            cell.setInteractive();
            cell.row = row;
            cell.col = col;
            
            cell.on('pointerover', function() {
                if (gameState.board[this.row][this.col] === '' && !gameState.gameOver) {
                    this.setStrokeStyle(2, 0x0000ff);
                }
            });
            
            cell.on('pointerout', function() {
                this.setStrokeStyle(0);
            });
            
            cell.on('pointerdown', function() {
                if (gameState.board[this.row][this.col] === '' && !gameState.gameOver) {
                    // Place marker
                    gameState.board[this.row][this.col] = gameState.currentPlayer;
                    
                    // Draw X or O
                    if (gameState.currentPlayer === 'X') {
                        drawX(self, cellX, cellY);
                    } else {
                        drawO(self, cellX, cellY);
                    }
                    
                    // Check for win
                    if (checkWin(self, this.row, this.col)) {
                        gameState.turnText.setText(`Player ${gameState.currentPlayer} wins!`);
                        gameState.gameOver = true;
                    } else if (checkDraw()) {
                        gameState.turnText.setText('Game Draw!');
                        gameState.gameOver = true;
                    } else {
                        // Switch player
                        gameState.currentPlayer = gameState.currentPlayer === 'X' ? 'O' : 'X';
                        gameState.turnText.setText(`Player ${gameState.currentPlayer} turn`);
                    }
                }
            });
        }
    }
    
    // Add reset button
    const resetButton = this.add.text(520, 50, 'Reset', { 
        fontSize: '24px', 
        fill: '#fff', 
        backgroundColor: '#4CAF50',
        padding: { left: 15, right: 15, top: 10, bottom: 10 }
    }).setOrigin(0.5).setInteractive();
    
    resetButton.on('pointerover', function() {
        this.setBackgroundColor('#45a049');
    });
    
    resetButton.on('pointerout', function() {
        this.setBackgroundColor('#4CAF50');
    });
    
    resetButton.on('pointerdown', function() {
        self.scene.restart();
    });
}

function drawX(scene, x, y) {
    const size = gameState.cellSize * 0.4;
    
    // Draw the X with line graphics
    const graphics = scene.add.graphics();
    graphics.lineStyle(8, 0xFF0000, 1);
    
    // First diagonal
    graphics.beginPath();
    graphics.moveTo(x - size, y - size);
    graphics.lineTo(x + size, y + size);
    graphics.closePath();
    graphics.strokePath();
    
    // Second diagonal
    graphics.beginPath();
    graphics.moveTo(x + size, y - size);
    graphics.lineTo(x - size, y + size);
    graphics.closePath();
    graphics.strokePath();
}

function drawO(scene, x, y) {
    const size = gameState.cellSize * 0.4;
    
    // Draw the O with circle graphics
    const graphics = scene.add.graphics();
    graphics.lineStyle(8, 0x0000FF, 1);
    graphics.strokeCircle(x, y, size);
}

function checkWin(scene, row, col) {
    const board = gameState.board;
    const player = gameState.currentPlayer;
    
    // Check row
    if (board[row][0] === player && board[row][1] === player && board[row][2] === player) {
        drawWinningLine(scene, 0, row, 2, row);
        return true;
    }
    
    // Check column
    if (board[0][col] === player && board[1][col] === player && board[2][col] === player) {
        drawWinningLine(scene, col, 0, col, 2);
        return true;
    }
    
    // Check diagonals
    if (board[0][0] === player && board[1][1] === player && board[2][2] === player) {
        drawWinningLine(scene, 0, 0, 2, 2);
        return true;
    }
    
    if (board[0][2] === player && board[1][1] === player && board[2][0] === player) {
        drawWinningLine(scene, 2, 0, 0, 2);
        return true;
    }
    
    return false;
}

function drawWinningLine(scene, startCol, startRow, endCol, endRow) {
    // Calculate the pixel positions
    const startX = gameState.gridOffset + startCol * gameState.cellSize + gameState.cellSize/2;
    const startY = gameState.gridOffset + startRow * gameState.cellSize + gameState.cellSize/2;
    const endX = gameState.gridOffset + endCol * gameState.cellSize + gameState.cellSize/2;
    const endY = gameState.gridOffset + endRow * gameState.cellSize + gameState.cellSize/2;
    
    // Draw the winning line
    const graphics = scene.add.graphics();
    graphics.lineStyle(5, 0x00FF00, 1);
    graphics.beginPath();
    graphics.moveTo(startX, startY);
    graphics.lineTo(endX, endY);
    graphics.closePath();
    graphics.strokePath();
}

function checkDraw() {
    for (let row = 0; row < 3; row++) {
        for (let col = 0; col < 3; col++) {
            if (gameState.board[row][col] === '') {
                return false;
            }
        }
    }
    return true;
}
"""

def _generate_snake_code(game_logic):
    """Generate Phaser.js code for Snake game"""
    return """
const config = {
    type: Phaser.AUTO,
    width: 640,
    height: 480,
    backgroundColor: '#bfcc00',
    physics: {
        default: 'arcade',
        arcade: {
            gravity: { y: 0 },
            debug: false
        }
    },
    scene: {
        preload: preload,
        create: create,
        update: update
    }
};

const gameState = {
    snake: null,
    food: null,
    cursors: null,
    speed: 100,
    lastMoveTime: 0,
    direction: { x: 1, y: 0 },
    nextDirection: { x: 1, y: 0 },
    snakeBody: [],
    gridSize: 20,
    score: 0,
    gameOver: false
};

const game = new Phaser.Game(config);

function preload() {
    // No assets to preload for the skeleton version
}

function create() {
    // Create snake head
    gameState.snake = this.add.rectangle(200, 200, gameState.gridSize, gameState.gridSize, 0x00ff00);
    gameState.snakeBody = [];
    
    // Create initial body segments (start with 2 segments)
    for (let i = 0; i < 2; i++) {
        const segment = this.add.rectangle(
            200 - ((i + 1) * gameState.gridSize), 
            200, 
            gameState.gridSize, 
            gameState.gridSize, 
            0x008800
        );
        gameState.snakeBody.push(segment);
    }
    
    // Create food
    gameState.food = this.add.rectangle(300, 300, gameState.gridSize, gameState.gridSize, 0xff0000);
    
    // Set up random food position
    placeFood.call(this);
    
    // Set up keyboard control
    gameState.cursors = this.input.keyboard.createCursorKeys();
    
    // Score text
    gameState.scoreText = this.add.text(16, 16, 'Score: 0', { fontSize: '24px', fill: '#000' });
    
    // Game over text
    gameState.gameOverText = this.add.text(320, 240, 'Game Over!\\nPress R to restart', { 
        fontSize: '32px', 
        fill: '#000', 
        align: 'center' 
    }).setOrigin(0.5);
    gameState.gameOverText.visible = false;
    
    // Restart key
    this.input.keyboard.on('keydown-R', function () {
        this.scene.restart();
    }, this);
}

function update(time) {
    // Game over check
    if (gameState.gameOver) return;
    
    // Handle input for direction change
    if (gameState.cursors.left.isDown && gameState.direction.x !== 1) {
        gameState.nextDirection = { x: -1, y: 0 };
    } else if (gameState.cursors.right.isDown && gameState.direction.x !== -1) {
        gameState.nextDirection = { x: 1, y: 0 };
    } else if (gameState.cursors.up.isDown && gameState.direction.y !== 1) {
        gameState.nextDirection = { x: 0, y: -1 };
    } else if (gameState.cursors.down.isDown && gameState.direction.y !== -1) {
        gameState.nextDirection = { x: 0, y: 1 };
    }
    
    // Move snake based on tick
    if (time >= gameState.lastMoveTime + gameState.speed) {
        gameState.lastMoveTime = time;
        moveSnake.call(this);
    }
}

function moveSnake() {
    // Update direction
    gameState.direction = gameState.nextDirection;
    
    // Calculate new position
    const snakeX = gameState.snake.x + gameState.direction.x * gameState.gridSize;
    const snakeY = gameState.snake.y + gameState.direction.y * gameState.gridSize;
    
    // Move body segments
    for (let i = gameState.snakeBody.length - 1; i > 0; i--) {
        gameState.snakeBody[i].x = gameState.snakeBody[i-1].x;
        gameState.snakeBody[i].y = gameState.snakeBody[i-1].y;
    }
    
    // If there's at least one body segment, move it to head's position
    if (gameState.snakeBody.length > 0) {
        gameState.snakeBody[0].x = gameState.snake.x;
        gameState.snakeBody[0].y = gameState.snake.y;
    }
    
    // Move head
    gameState.snake.x = snakeX;
    gameState.snake.y = snakeY;
    
    // Check collisions
    checkCollision.call(this);
    checkFoodCollision.call(this);
}

function checkCollision() {
    // Check wall collision
    if (gameState.snake.x < 0 || 
        gameState.snake.x >= config.width || 
        gameState.snake.y < 0 || 
        gameState.snake.y >= config.height) {
        gameOver.call(this);
        return;
    }
    
    // Check self collision
    for (let i = 0; i < gameState.snakeBody.length; i++) {
        if (gameState.snake.x === gameState.snakeBody[i].x && 
            gameState.snake.y === gameState.snakeBody[i].y) {
            gameOver.call(this);
            return;
        }
    }
}

function checkFoodCollision() {
    if (gameState.snake.x === gameState.food.x && 
        gameState.snake.y === gameState.food.y) {
        // Grow snake
        const lastSegment = gameState.snakeBody.length > 0 
            ? gameState.snakeBody[gameState.snakeBody.length - 1] 
            : gameState.snake;
            
        const newSegment = this.add.rectangle(
            lastSegment.x, 
            lastSegment.y, 
            gameState.gridSize, 
            gameState.gridSize, 
            0x008800
        );
        gameState.snakeBody.push(newSegment);
        
        // Update score
        gameState.score += 10;
        gameState.scoreText.setText(`Score: ${gameState.score}`);
        
        // Place new food
        placeFood.call(this);
        
        // Increase speed slightly
        gameState.speed = Math.max(50, gameState.speed - 1);
    }
}

function placeFood() {
    const gridWidth = Math.floor(config.width / gameState.gridSize);
    const gridHeight = Math.floor(config.height / gameState.gridSize);
    
    let foodX, foodY;
    let validPosition = false;
    
    // Keep generating positions until a valid one is found
    while (!validPosition) {
        foodX = Math.floor(Math.random() * gridWidth) * gameState.gridSize;
        foodY = Math.floor(Math.random() * gridHeight) * gameState.gridSize;
        
        validPosition = true;
        
        // Check if food is on snake head
        if (foodX === gameState.snake.x && foodY === gameState.snake.y) {
            validPosition = false;
            continue;
        }
        
        // Check if food is on snake body
        for (let i = 0; i < gameState.snakeBody.length; i++) {
            if (foodX === gameState.snakeBody[i].x && foodY === gameState.snakeBody[i].y) {
                validPosition = false;
                break;
            }
        }
    }
    
    // Set food position
    gameState.food.x = foodX;
    gameState.food.y = foodY;
}

function gameOver() {
    gameState.gameOver = true;
    gameState.gameOverText.visible = true;
}
"""

def _generate_pong_code(game_logic):
    """Generate Phaser.js code for Pong game"""
    return """
const config = {
    type: Phaser.AUTO,
    width: 800,
    height: 600,
    backgroundColor: '#000000',
    physics: {
        default: 'arcade',
        arcade: {
            gravity: { y: 0 },
            debug: false
        }
    },
    scene: {
        preload: preload,
        create: create,
        update: update
    }
};

const gameState = {
    player1Score: 0,
    player2Score: 0,
    gameOver: false,
    paddleSpeed: 5,
    scoreToWin: 11
};

const game = new Phaser.Game(config);

function preload() {
    // No assets to preload for skeleton version
}

function create() {
    // Store scene reference for callbacks
    const self = this;
    
    // Add center line
    const centerLine = this.add.graphics();
    centerLine.lineStyle(2, 0xffffff, 1);
    centerLine.beginPath();
    centerLine.moveTo(400, 0);
    centerLine.lineTo(400, 600);
    centerLine.strokePath();
    
    // Create paddles
    gameState.player1 = this.physics.add.sprite(50, 300, null);
    gameState.player1.body.setSize(15, 100);
    gameState.player1.body.immovable = true;
    gameState.player1.setCollideWorldBounds(true);
    
    gameState.player2 = this.physics.add.sprite(750, 300, null);
    gameState.player2.body.setSize(15, 100);
    gameState.player2.body.immovable = true;
    gameState.player2.setCollideWorldBounds(true);
    
    // Draw paddles
    gameState.paddlesGraphics = this.add.graphics({ name: 'paddlesGraphics' });
    updatePaddles();
    
    // Create ball
    gameState.ball = this.physics.add.sprite(400, 300, null);
    gameState.ball.body.setSize(10, 10);
    gameState.ball.body.bounce.set(1);
    gameState.ball.setCollideWorldBounds(true);
    
    // Draw ball
    gameState.ballGraphics = this.add.graphics({ name: 'ballGraphics' });
    updateBall();
    
    // Set initial ball velocity with delay
    launchBall.call(this);
    
    // Set up collisions
    this.physics.add.collider(gameState.ball, gameState.player1, hitPaddle, null, this);
    this.physics.add.collider(gameState.ball, gameState.player2, hitPaddle, null, this);
    
    // Add world bounds event for top and bottom
    gameState.ball.body.onWorldBounds = true;
    
    // Score
    gameState.player1Score = 0;
    gameState.player2Score = 0;
    gameState.scoreText1 = this.add.text(200, 50, '0', { fontSize: '64px', fill: '#fff' }).setOrigin(0.5);
    gameState.scoreText2 = this.add.text(600, 50, '0', { fontSize: '64px', fill: '#fff' }).setOrigin(0.5);
    
    // Controls
    gameState.cursors = this.input.keyboard.createCursorKeys();
    gameState.wasdKeys = this.input.keyboard.addKeys({
        up: Phaser.Input.Keyboard.KeyCodes.W,
        down: Phaser.Input.Keyboard.KeyCodes.S
    });
    
    // Game over text
    gameState.gameOverText = this.add.text(400, 300, '', { fontSize: '48px', fill: '#fff' }).setOrigin(0.5);
    gameState.gameOverText.visible = false;
    
    // Add restart key
    this.input.keyboard.on('keydown-R', function() {
        if (gameState.gameOver) {
            self.scene.restart();
        }
    }, this);
    
    // Instructions
    const instructions = this.add.text(400, 550, 'Player 1: W/S keys | Player 2: Up/Down arrows | R to restart', 
        { fontSize: '16px', fill: '#fff' }
    ).setOrigin(0.5);
}

function update() {
    if (gameState.gameOver) {
        return;
    }
    
    // Update paddle positions
    // Player 1 controls (WASD)
    if (gameState.wasdKeys.up.isDown) {
        gameState.player1.y -= gameState.paddleSpeed;
    } else if (gameState.wasdKeys.down.isDown) {
        gameState.player1.y += gameState.paddleSpeed;
    }
    
    // Player 2 controls (arrow keys)
    if (gameState.cursors.up.isDown) {
        gameState.player2.y -= gameState.paddleSpeed;
    } else if (gameState.cursors.down.isDown) {
        gameState.player2.y += gameState.paddleSpeed;
    }
    
    // Update graphics
    updatePaddles();
    updateBall();
    
    // Check for scoring
    checkBallBounds.call(this);
}

function updatePaddles() {
    gameState.paddlesGraphics.clear();
    gameState.paddlesGraphics.fillStyle(0xffffff, 1);
    gameState.paddlesGraphics.fillRect(gameState.player1.x - 7.5, gameState.player1.y - 50, 15, 100);
    gameState.paddlesGraphics.fillRect(gameState.player2.x - 7.5, gameState.player2.y - 50, 15, 100);
}

function updateBall() {
    gameState.ballGraphics.clear();
    gameState.ballGraphics.fillStyle(0xffffff, 1);
    gameState.ballGraphics.fillRect(gameState.ball.x - 5, gameState.ball.y - 5, 10, 10);
}

function checkBallBounds() {
    // Check for scoring
    if (gameState.ball.x < 0) {
        // Player 2 scores
        gameState.player2Score++;
        gameState.scoreText2.setText(gameState.player2Score);
        resetBall.call(this);
        checkWinCondition.call(this);
    } else if (gameState.ball.x > config.width) {
        // Player 1 scores
        gameState.player1Score++;
        gameState.scoreText1.setText(gameState.player1Score);
        resetBall.call(this);
        checkWinCondition.call(this);
    }
}

function checkWinCondition() {
    if (gameState.player1Score >= gameState.scoreToWin) {
        gameOver.call(this, 'PLAYER 1 WINS');
    } else if (gameState.player2Score >= gameState.scoreToWin) {
        gameOver.call(this, 'PLAYER 2 WINS');
    }
}

function gameOver(text) {
    gameState.gameOver = true;
    gameState.gameOverText.setText(text + '\\nPress R to restart');
    gameState.gameOverText.visible = true;
    this.physics.pause();
}

function hitPaddle(ball, paddle) {
    // Increase horizontal velocity when hit
    let velocityX = Math.abs(ball.body.velocity.x);
    velocityX = Math.min(velocityX + 20, 600); // Cap maximum speed
    
    // Calculate vertical angle based on where ball hit the paddle
    let diff = 0;
    if (paddle === gameState.player1) {
        // Right direction if hit player 1
        ball.body.setVelocityX(velocityX);
        diff = ball.y - paddle.y;
    } else {
        // Left direction if hit player 2
        ball.body.setVelocityX(-velocityX);
        diff = ball.y - paddle.y;
    }
    
    // Change vertical velocity based on where the ball hit the paddle
    // Middle of paddle = low angle, edges = high angle
    // Scale from -300 to 300 based on position
    const scaleFactor = 6;
    ball.body.setVelocityY(diff * scaleFactor);
}

function resetBall() {
    gameState.ball.setPosition(400, 300);
    launchBall.call(this);
}

function launchBall() {
    // Reset velocity
    gameState.ball.body.setVelocity(0);
    
    // Random direction with slight delay
    this.time.delayedCall(1000, function() {
        // Random direction (left or right)
        const velocityX = (Math.random() > 0.5 ? 1 : -1) * 300;
        // Random angle for Y velocity (-100 to 100)
        const velocityY = (Math.random() - 0.5) * 200;
        gameState.ball.body.setVelocity(velocityX, velocityY);
    }, [], this);
}
"""

def _generate_breakout_code(game_logic):
    """Generate Phaser.js code for Breakout game"""
    return """
const config = {
    type: Phaser.AUTO,
    width: 800,
    height: 600,
    backgroundColor: '#2d2d2d',
    physics: {
        default: 'arcade',
        arcade: {
            gravity: { y: 0 },
            debug: false
        }
    },
    scene: {
        preload: preload,
        create: create,
        update: update
    }
};

const gameState = {
    gameOver: false,
    lives: 3,
    score: 0,
    ballOnPaddle: true,
    brickInfo: {
        width: 70,
        height: 25,
        count: {
            row: 5,
            col: 8
        },
        offset: {
            top: 100,
            left: 120
        },
        padding: 10
    }
};

const game = new Phaser.Game(config);

function preload() {
    // No assets to preload for skeleton version
}

function create() {
    // Score and lives text
    gameState.scoreText = this.add.text(16, 16, 'Score: 0', { fontSize: '24px', fill: '#fff' });
    gameState.livesText = this.add.text(this.sys.game.config.width - 16, 16, 'Lives: 3', { fontSize: '24px', fill: '#fff' });
    gameState.livesText.setOrigin(1, 0);
    
    // Create paddle
    gameState.paddle = this.physics.add.sprite(400, 550, null);
    gameState.paddle.body.setSize(100, 20);
    gameState.paddle.body.immovable = true;
    gameState.paddle.setCollideWorldBounds(true);
    
    // Draw paddle
    gameState.paddleGraphics = this.add.graphics({ name: 'paddleGraphics' });
    gameState.paddleGraphics.fillStyle(0xffffff, 1);
    gameState.paddleGraphics.fillRect(gameState.paddle.x - 50, gameState.paddle.y - 10, 100, 20);
    
    // Create ball
    gameState.ball = this.physics.add.sprite(400, 530, null);
    gameState.ball.body.setSize(20, 20);
    gameState.ball.body.bounce.set(1);
    gameState.ball.body.collideWorldBounds = true;
    gameState.ball.setCollideWorldBounds(true);
    
    // Add world bounds event except for bottom
    gameState.ball.body.onWorldBounds = true;
    this.physics.world.on('worldbounds', function(body, up, down, left, right) {
        if (down) {
            lostBall.call(this);
        }
    }, this);
    
    // Draw ball
    gameState.ballGraphics = this.add.graphics({ name: 'ballGraphics' });
    gameState.ballGraphics.fillStyle(0xffffff, 1);
    gameState.ballGraphics.fillCircle(gameState.ball.x, gameState.ball.y, 10);
    
    // Create bricks
    gameState.bricks = this.physics.add.staticGroup();
    gameState.brickGraphics = this.add.graphics({ name: 'brickGraphics' });
    
    const brickColors = [0xff0000, 0xff7f00, 0xffff00, 0x00ff00, 0x0000ff];
    
    for (let y = 0; y < gameState.brickInfo.count.row; y++) {
        for (let x = 0; x < gameState.brickInfo.count.col; x++) {
            const brickX = gameState.brickInfo.offset.left + x * (gameState.brickInfo.width + gameState.brickInfo.padding);
            const brickY = gameState.brickInfo.offset.top + y * (gameState.brickInfo.height + gameState.brickInfo.padding);
            
            const brick = gameState.bricks.create(brickX, brickY, null);
            brick.body.setSize(gameState.brickInfo.width, gameState.brickInfo.height);
            brick.setData('color', brickColors[y]);
            
            // Draw brick
            gameState.brickGraphics.fillStyle(brickColors[y], 1);
            gameState.brickGraphics.fillRect(
                brickX - gameState.brickInfo.width/2, 
                brickY - gameState.brickInfo.height/2, 
                gameState.brickInfo.width, 
                gameState.brickInfo.height
            );
        }
    }
    
    // Set up collisions
    this.physics.add.collider(gameState.ball, gameState.bricks, hitBrick, null, this);
    this.physics.add.collider(gameState.ball, gameState.paddle, hitPaddle, null, this);
    
    // Controls
    gameState.cursors = this.input.keyboard.createCursorKeys();
    
    // Game over text
    gameState.gameOverText = this.add.text(400, 300, '', { fontSize: '48px', fill: '#fff', align: 'center' });
    gameState.gameOverText.setOrigin(0.5);
    gameState.gameOverText.visible = false;
    
    // Spacebar to start
    this.input.keyboard.on('keydown-SPACE', function() {
        if (gameState.ballOnPaddle) {
            gameState.ball.setVelocity(-75, -300);
            gameState.ballOnPaddle = false;
        }
    }, this);
    
    // Display instructions
    const instructions = this.add.text(400, 450, 'Press SPACEBAR to launch the ball\nUse LEFT/RIGHT arrows to move paddle', 
        { fontSize: '18px', fill: '#fff', align: 'center' }
    );
    instructions.setOrigin(0.5);
}

function update() {
    if (gameState.gameOver) {
        return;
    }
    
    // Move paddle with cursor keys
    if (gameState.cursors.left.isDown) {
        gameState.paddle.x -= 7;
        if (gameState.ballOnPaddle) {
            gameState.ball.x -= 7;
        }
    } else if (gameState.cursors.right.isDown) {
        gameState.paddle.x += 7;
        if (gameState.ballOnPaddle) {
            gameState.ball.x += 7;
        }
    }
    
    // Keep paddle on screen
    gameState.paddle.x = Phaser.Math.Clamp(gameState.paddle.x, 50, config.width - 50);
    
    // Redraw paddle
    gameState.paddleGraphics.clear();
    gameState.paddleGraphics.fillStyle(0xffffff, 1);
    gameState.paddleGraphics.fillRect(gameState.paddle.x - 50, gameState.paddle.y - 10, 100, 20);
    
    // Redraw ball at new position
    gameState.ballGraphics.clear();
    gameState.ballGraphics.fillStyle(0xffffff, 1);
    gameState.ballGraphics.fillCircle(gameState.ball.x, gameState.ball.y, 10);
    
    if (gameState.ballOnPaddle) {
        gameState.ball.setPosition(gameState.paddle.x, gameState.paddle.y - 20);
    }
}

function hitBrick(ball, brick) {
    brick.disableBody(true, true);
    
    // Remove brick from graphics
    const brickX = brick.x;
    const brickY = brick.y;
    const color = brick.getData('color');
    
    // Redraw bricks (clear and redraw all remaining bricks)
    updateBrickGraphics.call(this);
    
    gameState.score += 10;
    gameState.scoreText.setText('Score: ' + gameState.score);
    
    // Check if all bricks are gone
    if (gameState.bricks.countActive() === 0) {
        gameWin.call(this);
    }
}

function updateBrickGraphics() {
    // Clear and redraw all bricks
    gameState.brickGraphics.clear();
    
    gameState.bricks.getChildren().forEach(function(brick) {
        if (brick.active) {
            gameState.brickGraphics.fillStyle(brick.getData('color'), 1);
            gameState.brickGraphics.fillRect(
                brick.x - gameState.brickInfo.width/2, 
                brick.y - gameState.brickInfo.height/2, 
                gameState.brickInfo.width, 
                gameState.brickInfo.height
            );
        }
    });
}

function hitPaddle(ball, paddle) {
    // Calculate relative position of ball on paddle (-1 to 1)
    const diff = ball.x - paddle.x;
    
    if (diff < 0) {
        // Left side of paddle
        ball.body.setVelocityX(10 * diff);
    } else if (diff > 0) {
        // Right side of paddle
        ball.body.setVelocityX(10 * diff);
    } else {
        // Center of paddle
        ball.body.setVelocityX(2 + Math.random() * 8);
    }
}

function lostBall() {
    gameState.lives--;
    gameState.livesText.setText('Lives: ' + gameState.lives);
    
    if (gameState.lives === 0) {
        gameOver.call(this);
    } else {
        gameState.ballOnPaddle = true;
        gameState.ball.setVelocity(0, 0);
    }
}

function gameOver() {
    gameState.gameOver = true;
    gameState.ball.setVelocity(0, 0);
    gameState.gameOverText.setText('GAME OVER\nPress R to restart');
    gameState.gameOverText.visible = true;
    
    this.input.keyboard.once('keydown-R', function() {
        this.scene.restart();
    }, this);
}

function gameWin() {
    gameState.gameOver = true;
    gameState.ball.setVelocity(0, 0);
    gameState.gameOverText.setText('YOU WIN!\nPress R to restart');
    gameState.gameOverText.visible = true;
    
    this.input.keyboard.once('keydown-R', function() {
        this.scene.restart();
    }, this);
}
"""

def _generate_collector_code(game_logic):
    """Generate Phaser.js code for a simple collector game"""
    return """
const config = {
    type: Phaser.AUTO,
    width: 800,
    height: 600,
    backgroundColor: '#4488aa',
    physics: {
        default: 'arcade',
        arcade: {
            gravity: { y: 0 },
            debug: false
        }
    },
    scene: {
        preload: preload,
        create: create,
        update: update
    }
};

const gameState = {
    score: 0,
    gameOver: false,
    totalItems: 10,
    collectedItems: 0,
    playerSpeed: 200
};

const game = new Phaser.Game(config);

function preload() {
    // No assets to preload for skeleton version
}

function create() {
    // Score text
    gameState.scoreText = this.add.text(16, 16, 'Score: 0', { fontSize: '24px', fill: '#fff' });
    
    // Create player
    gameState.player = this.physics.add.sprite(400, 300, null);
    gameState.player.body.setSize(32, 32);
    
    // Draw player
    const playerGraphics = this.add.graphics();
    playerGraphics.fillStyle(0xffff00, 1);
    playerGraphics.fillCircle(gameState.player.x, gameState.player.y, 16);
    playerGraphics.setName('playerGraphics');
    
    // Create items
    gameState.items = this.physics.add.group();
    
    // Create obstacles
    gameState.obstacles = this.physics.add.staticGroup();
    
    // Create random items
    for (let i = 0; i < gameState.totalItems; i++) {
        const x = Phaser.Math.Between(50, config.width - 50);
        const y = Phaser.Math.Between(50, config.height - 50);
        
        const item = gameState.items.create(x, y, null);
        item.body.setSize(24, 24);
        
        // Draw item
        const itemGraphics = this.add.graphics();
        itemGraphics.fillStyle(0x00ff00, 1);
        itemGraphics.fillRect(x - 12, y - 12, 24, 24);
    }
    
    // Create random obstacles
    for (let i = 0; i < 5; i++) {
        const x = Phaser.Math.Between(100, config.width - 100);
        const y = Phaser.Math.Between(100, config.height - 100);
        const width = Phaser.Math.Between(50, 100);
        const height = Phaser.Math.Between(20, 60);
        
        const obstacle = gameState.obstacles.create(x, y, null);
        obstacle.body.setSize(width, height);
        
        // Draw obstacle
        const obstacleGraphics = this.add.graphics();
        obstacleGraphics.fillStyle(0xff0000, 1);
        obstacleGraphics.fillRect(x - width/2, y - height/2, width, height);
    }
    
    // Set up collisions
    this.physics.add.overlap(gameState.player, gameState.items, collectItem, null, this);
    this.physics.add.collider(gameState.player, gameState.obstacles, hitObstacle, null, this);
    
    // Controls
    gameState.cursors = this.input.keyboard.createCursorKeys();
    
    // Game over text
    gameState.gameOverText = this.add.text(400, 300, '', { fontSize: '48px', fill: '#fff', align: 'center' });
    gameState.gameOverText.setOrigin(0.5);
    gameState.gameOverText.visible = false;
}

function update() {
    if (gameState.gameOver) {
        return;
    }
    
    // Player movement
    gameState.player.setVelocity(0);
    
    if (gameState.cursors.left.isDown) {
        gameState.player.setVelocityX(-gameState.playerSpeed);
    } else if (gameState.cursors.right.isDown) {
        gameState.player.setVelocityX(gameState.playerSpeed);
    }
    
    if (gameState.cursors.up.isDown) {
        gameState.player.setVelocityY(-gameState.playerSpeed);
    } else if (gameState.cursors.down.isDown) {
        gameState.player.setVelocityY(gameState.playerSpeed);
    }
    
    // Update player graphics position
    this.children.getByName('playerGraphics')?.destroy();
    const playerGraphics = this.add.graphics({ name: 'playerGraphics' });
    playerGraphics.fillStyle(0xffff00, 1);
    playerGraphics.fillCircle(gameState.player.x, gameState.player.y, 16);
}

function collectItem(player, item) {
    item.disableBody(true, true);
    
    // Update score
    gameState.score += 10;
    gameState.scoreText.setText('Score: ' + gameState.score);
    
    // Update collected items counter
    gameState.collectedItems++;
    
    // Check win condition
    if (gameState.collectedItems >= gameState.totalItems) {
        gameWin.call(this);
    }
}

function hitObstacle(player, obstacle) {
    this.physics.pause();
    
    gameState.gameOver = true;
    gameState.gameOverText.setText('GAME OVER\nPress R to restart');
    gameState.gameOverText.visible = true;
    
    this.input.keyboard.once('keydown-R', function() {
        this.scene.restart();
    }, this);
}

function gameWin() {
    this.physics.pause();
    
    gameState.gameOver = true;
    gameState.gameOverText.setText('YOU WIN!\nPress R to restart');
    gameState.gameOverText.visible = true;
    
    this.input.keyboard.once('keydown-R', function() {
        this.scene.restart();
    }, this);
}
""" 