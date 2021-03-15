const twc = document.getElementById('twc');
const aa = document.getElementById('aa');
const knw1 = document.getElementById('knw1');
const knw2 = document.getElementById('knw2');
const twc1 = document.getElementById('twc1');
const aa1 = document.getElementById('aa1');
const knw11 = document.getElementById('knw11');
const knw21 = document.getElementById('knw21');

async function getData() {
    const response = await fetch('/getstatus');
    const data = await response.json();
    twc.innerHTML = data.twc[0];
    aa.innerHTML = data.aa[0];
    knw1.innerHTML = data.knw1[0];
    knw2.innerHTML = data.knw2[0];
    twc1.innerHTML = data.twc[1];
    aa1.innerHTML = data.aa[1];
    knw11.innerHTML = data.knw1[1];
    knw21.innerHTML = data.knw2[1];
}

function getStatus() {
    getData();
    return (setInterval(getData, 20000));
}