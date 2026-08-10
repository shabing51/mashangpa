import axios from "axios";
import { sm2 } from "sm-crypto";

const publicKey =
"04064c2a3bcafba2c1ca4f5fb8ecd876b23d70fc4479b78f3c8066c02a8c17749458bca86361bc563d2501b61e2ac93a676a1305893aafcc6be2ea48ecb048672e";

function doEncrypt(data){
    return sm2.doEncrypt(data,publicKey,1);
}

let e = {
    Trip:[
        {
            Date:"2026-09-02",
            Dep:"PEK",
            Arrival:"CKG"
        }
    ],
    Passenger:{
        adult:1,
        child:0,
        baby:0
    },
    notchType:null,
    aimPrice:null,
    RequestParameterSecurityIdentificationBit:true
};

function getParams(e){
    let t = encodeURIComponent(
        JSON.stringify(e)
    );
    return doEncrypt(t);
}

async function getAirChinaData(){
    let params = getParams(e);
    let data = {
        params: params,
        RequestParameterEncryptionIdentificationBit:true
    };

    let headers = {
        "accept":
        "application/json, text/plain, */*",
        "content-type":
        "application/json",
        "origin":"https://www.airchina.com.cn",
        "referer":
        "https://www.airchina.com.cn/flight/oneway/pek-ckg/2026-08-28",
        "user-agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/150.0.0.0 Safari/537.36",
        "x-locale":"zh-CN",
        "x-device-token":
        "tak01j5DYI2WYUKANYZKVNEAMEDDKD4MRIABVCOF3ET2B5KPLXM5QVXYETJCAG3QROXIQ54IWNV6GTTH6UJYKOB5LOOKTYBEJNGFJGUNO3B42HQR5OHHSZULAUDUXLYVTNFDTYKVLZ4XCJIYQSEMOWTAJJ622ZYD4Q"
    };

    let cookies = {
        HWWAFSESTIME:"1785749664172",
        HWWAFSESID:"c34c982a085e838b06",
        ariaappid:"1cea560ed256bea7ae52761bd9042164"
    };
    let resp = await axios.post(
        "https://www.airchina.com.cn/gateway/api/flight/list",
        data,
        {
            headers,
            cookies
        }
    );
    console.log(JSON.stringify(resp.data, null, 2));
}
getAirChinaData();

// console.log(getParams(e));