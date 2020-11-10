let speed = 20;
let scale = .1;
//Math.min(window.innerWidth, window.innerHeight) * 0.25;
let canvas;
let ctx;
let logoColor;
window.addEventListener("resize", ()=>{
    head.x = Math.floor((window.innerWidth - 250) / 2);
    head.y = Math.floor((window.innerHeight - 250) / 5);
}
);

let head = {
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
    head.img.src = "https://i.bulbe.rocks/assets/bulb.png";

    update();
}
)();

function update() {
    setTimeout(()=>{
        //Draw the "tv screen"
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        //Draw the canvas background
        ctx.fillStyle = '#fff';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        //Draw DVD Logo and his background
        ctx.fillStyle = logoColor;
        //ctx.fillRect(head.x, head.y, head.img.width * scale, head.img.height * scale);
		head.theta += head.thetaSpeed;
        drawImageCenter(head.img, head.x, head.y, head.img.width/2, head.img.height/2, scale, head.theta);
		ctx.setTransform(1,0,0,1,0,0); // which is much quicker than save and restore
        //Move the logo
        head.x += head.xSpeed;
        head.y += head.ySpeed;
        //Check for collision
        checkHitBox();
        update();
    }
    , speed)
}

// same as above but cx and cy are the location of the point of rotation
// in image pixel coordinates
function drawImageCenter(image, x, y, cx, cy, scale, rotation){
    ctx.setTransform(scale, 0, 0, scale, x, y); // sets scale and origin
    ctx.rotate(rotation);
    ctx.drawImage(image, -cx, -cy);
} 

//Check for border collision
function checkHitBox() {
    if (head.x + head.img.width * scale/2 >= canvas.width || head.x <= 0 + head.img.width*scale/2) {
        head.xSpeed *= -1;
    }

    if (head.y + head.img.height * scale/2 >= canvas.height || head.y <= 0 + head.img.height*scale/2) {
        head.ySpeed *= -1;
    }
}
