let twc = document.getElementById('twc');
let aa = document.getElementById('aa');
let knw1 = document.getElementById('knw1');
let knw2 = document.getElementById('knw2');

async function getData() {
    const response = await fetch('/getstatus');
    const data = await response.json();
    twc.innerHTML = data.twc;
    aa.innerHTML = data.aa;
    knw1.innerHTML = data.knw1;
    knw2.innerHTML = data.knw2;
}

function getStatus() {
    getData();
    return (setInterval(getData, 60000));
}