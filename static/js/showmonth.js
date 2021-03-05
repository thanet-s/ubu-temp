const months = {
    '1': 'มกราคม',
    '2': 'กุมภาพันธ์',
    '3': 'มีนาคม',
    '4': 'เมษายน',
    '5': 'พฤษภาคม',
    '6': 'มิถุนายน',
    '7': 'กรกฎาคม',
    '8': 'สิงหาคม',
    '9': 'กันยายน',
    '10': 'ตุลาคม',
    '11': 'พฤศจิกายน',
    '12': 'ธันวาคม',
}
const inject = document.getElementById("inject");

function monthFilter(mArr) {
    const availableMonth = Object.keys(months)
        .filter(key => mArr.includes(key))
        .reduce((obj, key) => {
            obj[key] = months[key];
            return obj;
        }, {});
    for (const [key, value] of Object.entries(availableMonth)) {
        inject.innerHTML += `<option value=${key}>${value}</option>`;
    }
}