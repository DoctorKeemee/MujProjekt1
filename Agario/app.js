
let scene, camera, renderer, player, start, particles = [], enemies = [];
const particleCount = 100;
const particleSize = 0.5;
const enemyCount = 10;
const enemySize = 0.2;
const playerSpeed = 0.05;
let playerSpeedX = 0;
let playerSpeedY = 0;
let gameField = 20;

function init() {
  scene = new THREE.Scene();
  camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
  camera.position.z = 5;

  renderer = new THREE.WebGLRenderer();
  renderer.setSize(window.innerWidth, window.innerHeight);
  document.body.appendChild(renderer.domElement);
    start = Date.now();

    //hrac
    const playerGeometry = new THREE.SphereGeometry(1, 32,32);
    const playerMaterial = new THREE.MeshBasicMaterial({ color: 0x0077ff });
    player = new THREE.Mesh(playerGeometry, playerMaterial);
    scene.add(player);

    //castice
    const particleGeometry = new THREE.SphereGeometry(particleSize, 32, 32);
    const particleMaterial = new THREE.MeshBasicMaterial({ color: 0xff8800 });

    for (let i = 0; i < particleCount; i++) {
        const particle = new THREE.Mesh(particleGeometry, particleMaterial);
        particle.position.set(Math.random() * gameField -1*gameField/2, Math.random() * gameField -1*gameField/2, 0)
        particles.push(particle);
        scene.add(particle);
    }

    //enemy
    const enemyParticleGeometry = new THREE.SphereGeometry(enemySize, 32, 32);
    const enemyParticleMaterial = new THREE.MeshBasicMaterial({ color: 0xff0000 });

    for (let i = 0; i < enemyCount; i++) {
        const enemy = new THREE.Mesh(enemyParticleGeometry, enemyParticleMaterial);
        enemy.position.set(Math.random() * 20 -10, Math.random() * 20 -10, 0)
        enemies.push(enemy);
        scene.add(enemy);
    }

    window.addEventListener('keydown', onKeyDown, false);

  animate();
}


function onKeyDown(event) {
    switch (event.keyCode) {
        case 87:
            playerSpeedY = playerSpeed;
            break;
        case 83:
            playerSpeedY = -playerSpeed;
            break;
        case 65:
            playerSpeedX = -playerSpeed;
            break;
        case 68:
            playerSpeedX = playerSpeed;
            break;
            //add arrow keys
        case 38:
            playerSpeedY = playerSpeed;
            break;
        case 40:
            playerSpeedY = -playerSpeed;
            break;
        case 37:
            playerSpeedX = -playerSpeed;
            break;
        case 39:
            playerSpeedX = playerSpeed;
            break;
    }
}

function animate() {
    requestAnimationFrame(animate);

    camera.position.x = player.position.x;
    camera.position.y = player.position.y;
    let yDownCords = -1*gameField/2+player.scale.y;

    let newYPosiition = player.position.y + playerSpeedY;
    let newXPosition = player.position.x +  playerSpeedX;

    if(yDownCords>=newYPosiition){
        player.position.y = yDownCords;
        playerSpeedY = 0;
    }
    let xRightCords = -1*gameField/2+player.scale.x;
    if(xRightCords>=newXPosition){
        player.position.x = xRightCords;
        playerSpeedX = 0;
    }
    let yTopCords = gameField/2-player.scale.y;
    if(yTopCords<=newYPosiition){
        player.position.y = yTopCords;
        playerSpeedY = 0;
    }
    let xLeftCords = gameField/2-player.scale.x;
    if(xLeftCords<=newXPosition){
        player.position.x = xLeftCords;
        playerSpeedX = 0;
    }

    player.position.y += playerSpeedY;
    player.position.x += playerSpeedX;
    //if player is bigger camera is farer
    camera.position.z = 5 + player.scale.x*2;


    let enemyHit = false;
    enemies.forEach((enemy, index) => {
        const distance = player.position.distanceTo(enemy.position);
        //contanct detection particle size is 32, 32 count with player size
        let isColliding = distance < player.scale.x;

        const elapsedTime = Date.now() - start;
        if (isColliding && (enemyHit || elapsedTime>500)) {
            player.scale.x -= 0.1;
            player.scale.y -= 0.1;
            start = Date.now();
            enemyHit = true;
        }
    });

    particles.forEach((particle, index) => {
        const distance = player.position.distanceTo(particle.position);
        //contanct detection particle size is 32, 32 count with player size
        let isColliding = distance < player.scale.x;

        if (isColliding) {
            scene.remove(particle);
            particles.splice(index, 1);
            player.scale.x += 0.1;
            player.scale.y += 0.1;
        }
    });

    renderer.render(scene, camera);
}

window.onload = init;