let speed = 20;
let scale = .05;
let canvas;
let ctx;
let logoColor;
window.addEventListener("resize", ()=>{
    bulbe.x = Math.floor((window.innerWidth - 250) / 2);
    bulbe.y = Math.floor((window.innerHeight - 250) / 5);
}
);

let bulbe = {
    x: Math.floor((window.innerWidth - 250) / 2),
    y: Math.floor((window.innerHeight - 250) / 5),
    theta: 0,
	xSpeed: 5,
    ySpeed: 5,
	thetaSpeed: .01,
    img: new Image()
};

(function main() {
    canvas = document.getElementById("background");
    ctx = canvas.getContext("2d");
    bulbe.img.src = "https://i.bulbe.rocks/assets/bulb.png";
    update();
}
)();

function update() {
    setTimeout(()=>{
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
		bulbe.theta += bulbe.thetaSpeed;
        drawImageCenter(bulbe.img, bulbe.x, bulbe.y, bulbe.img.width/2, bulbe.img.height/2, scale, bulbe.theta);
		ctx.setTransform(1,0,0,1,0,0);
        bulbe.x += bulbe.xSpeed;
        bulbe.y += bulbe.ySpeed;
        checkHitBox();
        update();
    }
    , speed)
}

function drawImageCenter(image, x, y, cx, cy, scale, rotation){
    ctx.setTransform(scale, 0, 0, scale, x, y);
    ctx.rotate(rotation);
    ctx.drawImage(image, -cx, -cy);
} 

function checkHitBox() {
    if (bulbe.x + bulbe.img.width * scale/2 >= canvas.width || bulbe.x <= 0 + bulbe.img.width*scale/2) {
        bulbe.xSpeed *= -1;
    }

    if (bulbe.y + bulbe.img.height * scale/2 >= canvas.height || bulbe.y <= 0 + bulbe.img.height*scale/2) {
        bulbe.ySpeed *= -1;
    }
}
