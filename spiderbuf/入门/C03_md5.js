// 源代码部分变量字段经过unicode编码  // https://www.toolhelper.cn/EncodeDecode/UnicodeChinese
// 还需要扣md5这个函数，控制台测试知道是标准的md5 md5('123456') = 'e10adc3949ba59abbe56e057f20f883e'
// 这里没扣，因为网页里找到MD5源文件直接下载
md5 = require("C:/PycharmProjects/PythonProject/spiderbuf/md5.min.js")

function getIrisData(_0x3d0eeb) { // 函数参数就是页码
	const _0x1fa068 = Math["floor"](Math["random"]() * (0xba7af ^ 0xbb8ef) + (0xbe628 ^ 0xbe1f8));
	const _0x542b78 = Math["floor"](Date["now"]() / (0x54458 ^ 0x547b0));
	const _0x39669e = _0x3d0eeb ^ _0x542b78;
	const _0x56e6b4 = md5('' + _0x39669e + _0x542b78)["toString"]();
	const _0x811850 = {
		"xorResult": _0x39669e,
		'random': _0x1fa068,
		"timestamp": _0x542b78,
		"hash": _0x56e6b4
	};
//	fetch("scraper-practice-c03", {
//		"method": 'POST',
//		'body': JSON["stringify"](_0x811850)
//	})["then"](_0x227e76 => {
//		return _0x227e76['json']();
//	})['then'](_0xebb97e => {
//		const _0x398058 = document["querySelector"]('#flightTable\x20tbody');
//		_0x398058['innerHTML'] = '';
//		_0xebb97e['forEach']((_0x6aa98b, _0x2a8b82) => {
//			const _0x393a48 = document['createElement']("tr");
//			_0x393a48["innerHTML"] = '\x0a\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20<td>' + (_0x2a8b82 + (0xdc2fa ^ 0xdc2fb)) + '</td>\x0a\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20<td>' + _0x6aa98b['sepal_length'] + '</td>\x0a\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20<td>' + _0x6aa98b['sepal_width'] + '</td>\x0a\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20<td>' + _0x6aa98b['petal_length'] + '</td>\x0a\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20<td>' + _0x6aa98b['petal_width'] + '</td>\x0a\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20<td>' + _0x6aa98b["class"] + '</td>\x0a\x20\x20\x20\x20\x20\x20\x20\x20';
//			_0x398058['appendChild'](_0x393a48);
//		});
//	});  // 直接返回我们需要的请求参数即可,用python 发请求。

    return _0x811850
}

// Test
//console.log(getIrisData(3))



// AI 加了注释

//function getIrisData(_0x3d0eeb) {  // _0x3d0eeb = 页码
//    // 生成随机数（范围大约 0xba7af^0xbb8ef = 1000 左右）
//    const _0x1fa068 = Math["floor"](Math["random"]() * (0xba7af ^ 0xbb8ef) + (0xbe628 ^ 0xbe1f8));
//
//    // 生成时间戳（秒级）
//    const _0x542b78 = Math["floor"](Date["now"]() / (0x54458 ^ 0x547b0));
//    // 0x54458 ^ 0x547b0 = 1000，所以是毫秒转秒
//
//    // XOR 加密：页码 ^ 时间戳
//    const _0x39669e = _0x3d0eeb ^ _0x542b78;
//
//    // MD5加密：md5(xor结果 + 时间戳)
//    const _0x56e6b4 = md5('' + _0x39669e + _0x542b78)["toString"]();
//
//    // 返回请求参数
//    return {
//        "xorResult": _0x39669e,   // 页码 XOR 时间戳
//        'random': _0x1fa068,      // 随机数（实际未使用）
//        "timestamp": _0x542b78,   // 时间戳（秒）
//        "hash": _0x56e6b4         // MD5签名
//    }
//}


//fetch("scraper-practice-c03", {  // 请求URL（相对路径）
//    "method": 'POST',
//    'body': JSON.stringify(_0x811850)  // 发送上面生成的参数
//})
//.then(response => response.json())      // 解析JSON响应
//.then(data => {
//    // 获取表格body元素
//    const tbody = document.querySelector('#flightTable tbody');
//    tbody.innerHTML = '';  // 清空表格
//
//    // 遍历数据，生成表格行
//    data.forEach((item, index) => {
//        const tr = document.createElement("tr");
//        tr.innerHTML = `
//            <td>${index + 1}</td>
//            <td>${item.sepal_length}</td>
//            <td>${item.sepal_width}</td>
//            <td>${item.petal_length}</td>
//            <td>${item.petal_width}</td>
//            <td>${item.class}</td>
//        `;
//        tbody.appendChild(tr);
//    });
//});