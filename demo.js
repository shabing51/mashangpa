import CryptoJS from "crypto-js";
import axios from "axios";

function aesCBCEncrypt(plainText) {
  const key = "8080808080808080";
  const iv = "8080808080808080";
  const encrypted = CryptoJS.AES.encrypt(plainText, CryptoJS.enc.Utf8.parse(key), {
    iv: CryptoJS.enc.Utf8.parse(iv),
    mode: CryptoJS.mode.CBC,
    padding: CryptoJS.pad.Pkcs7
  });
  return encrypted.toString();
}

console.log(aesCBCEncrypt(
    JSON.stringify(
        {
            "from": "IBA",
            "to": "ABV",
            "start": "2026/08/03",
            "end": "2026/08/06",
            "return": "2026/08/06",
            "couponcode": "",
            "adults": 1,
            "child": 0,
            "infant": 0,
            "isRoundTrip": true,
            "manage": false,
            "recurrent": false
        }
    )
));
function getSessionId() {
    let d = aesCBCEncrypt(
        JSON.stringify({
            "from": "IBA",
            "to": "ABV",
            "start": "2026/08/03",
            "end": "2026/08/06",
            "return": "2026/08/06",
            "couponcode": "",
            "adults": 1,
            "child": 0,
            "infant": 0,
            "isRoundTrip": true,
            "manage": false,
            "recurrent": false
        })
    );
    return "".concat(d.substring(0, 50)).concat(Math.random());
}

async function fetchData() {
    let resp = await axios.post(
        "https://middleware.greenafrica.com/api/flight/getFlightLowFare", 
        {
            "from":"IBA",
            "couponcode":"",
            "to":"ABV",
            "startdate":"2026/08/01",
            "enddate":"2026/08/07",
            "child":0,
            "adults":1,
            "source":"",
            "currency":"NGN",
            "cabinCode":"ECO"
        },
        {
            headers:{
                "sessionid": getSessionId()
            }
        }
    );
    console.log(resp.data);
}

fetchData()