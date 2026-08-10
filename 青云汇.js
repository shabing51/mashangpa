import axios from "axios";
import CryptoJS from "crypto-js";

function dec(encryptedHex){
    let iv = "0012345900000678";
    let key = "0$0H_3p4$567890F0Kd0?123456789$@";
    let ciphertext = CryptoJS.enc.Hex.parse(encryptedHex);
    let cipherParams = CryptoJS.lib.CipherParams.create({
        ciphertext:ciphertext
    });
    let decData = CryptoJS.AES.decrypt(
        cipherParams,
        CryptoJS.enc.Utf8.parse(key),
        {
            iv: CryptoJS.enc.Utf8.parse(iv),
            mode: CryptoJS.mode.CBC,
            padding: CryptoJS.pad.Pkcs7
        }
    );

    return JSON.parse(decData.toString(CryptoJS.enc.Utf8));
}

async function getData(pageNum) {
    let url = "https://www.up678.com/dataserver/school/list"
    let resp = await axios.post(url, {
            "keywords": "",
            "provinces": "5,8",
            "type": "",
            "properties": "",
            "times": "",
            "yxts": "",
            "pageNo": pageNum.toString(),
            "_t": (new Date).getTime().toString()
        }
    )
    console.log(pageNum);
    return {"detail": dec(resp.data.datas), "describe": dec(resp.data.data)};
}


console.log(await getData(2));


