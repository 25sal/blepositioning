
var random=0;
function setBleCamera(){
    const camera = document.querySelector('#myCamera');

    if(random==0)
        camera.setAttribute('position', {x: camera.object3D.position.x, y: camera.object3D.position.y, z: camera.object3D.position.z+1});
    else
    camera.setAttribute('position', {x: camera.object3D.position.x, y: camera.object3D.position.y, z: camera.object3D.position.z-1});

     random = (random+1)%2;

}

setInterval(() => {
    //currentLon += step; // Move slightly east
    setBleCamera();
  }, 3000); // Every 3 seconds






