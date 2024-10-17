
var random=0;

async function getMyPosition() {
    try {
        const response = await fetch('api-service/position?id=1'); // Aspetta la risposta della fetch
        if (!response.ok) {
            throw new Error(`Errore nella richiesta: ${response.status} - ${response.statusText}`);
        }
        return await response.json(); // Aspetta la conversione della risposta in JSON e assegna alla variabile
    } catch (error) {
        console.error('Errore:', error); // Gestione errori
        return null; // Restituisce null in caso di errore
    }
}


function setBleCamera(){
    const camera = document.querySelector('#myCamera');
    getMyPosition().then((position) => {
        console.log(position);
        //camera.setAttribute('position', {x: position.x, y: position.y, z: position.z});
    });
    
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






