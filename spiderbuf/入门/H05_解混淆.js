//var _0x5b5a = ['a2JLbWk=', 'UG53dWQ=', 'bkFFSFY=', 'dGFibGU=', 'XihbXiBdKyggK1teIF0rKSspK1teIF19', 'NXwwfDF8Mnw0fDl8OHw3fDZ8Mw==', 'dHJ1bmM=', 'Z3NBamE=', 'aUliTVA=', 'QXljVHM=', 'dXNlZF9jb3VudA==', 'dGltZV90b19jcmFja19pdA==', 'dHJhY2U=', 'bG9n', 'U2ZmRlo=', 'bFhPTkw=', 'c3BsaXQ=', 'cmV0dXJuIChmdW5jdGlvbigpIA==', 'bVJ2SFM=', 'ZXhjZXB0aW9u', 'aW5uZXJUZXh0', 'aW5mbw==', 'S0hjSGQ=', 'WFl6bFg=', 'dGVzdA==', 'cmFua2luZw==', 'ZGF0YUNvbnRlbnQ=', 'RUZZQnM=', 'dGhlbg==', 'Z2V0VGltZQ==', 'MHwzfDJ8MXw1fDd8Nnw0', 'dHRGYXQ=', 'bFFEQm0=', 'V3dvWG4=', 'cGFzc3dk', 'TXloUnA=', 'aW5zZXJ0Um93', 'QlJWWUk=', 'ZXJyb3I=', 'aU13RWI=', 'anNvbg==', 'TWRxbEY=', 'd2Fybg==', 'Z2V0RWxlbWVudEJ5SWQ=', 'NHwzfDV8MHwyfDd8OHwxfDY=', 'aW5zZXJ0Q2VsbA==', 'Y29uc29sZQ==', 'Zm9yRWFjaA==', 'MXwyfDd8NHw2fDB8NXwz', 'WVVxYUY=', 'YXBwbHk=', 'Z3pqbEo=', 'ZGVidWc=', 'cmV0dXJuIC8iICsgdGhpcyArICIv', 'QlRaSGY='];
//var map = {};
//for (var i = 0; i < _0x5b5a.length; i++) {
//    map[i.toString(16)] = atob(_0x5b5a[i]);
//}

//// 特征识别表
//特征代码                          混淆类型
//─────────────────────────────────────────────────
//atob(_0x5b5a[i])                  → 字符串加密
//while(!![]){ switch(...) }        → 控制流平坦化
//function(){...}();                → 自执行函数
//navigator.webdriver               → 反检测
//_0x1d6c('0x3f')                   → 字符串索引
//var _0x254b44 = function() {...}  → 死代码注入

/*1. 字符串提取 → 存入数组，Base64 编码
    ↓
2. 变量名替换 → 生成无意义名称 (_0x5b5a, _0x1d6c)
    ↓
3. 控制流平坦化 → forEach 变成 switch 乱序
    ↓
4. 死代码注入 → 添加永不执行的分支
    ↓
5. 反调试注入 → 添加检测代码
    ↓
6. 自执行函数包装 → (function(){...})()
    ↓
混淆后代码*/


// 简化版混淆器实现
function simpleObfuscate(code) {
    // 1. 提取字符串
    const strings = [];
    const stringMap = new Map();

    code = code.replace(/['"]([^'"]+)['"]/g, (match, str) => {
        if (!stringMap.has(str)) {
            stringMap.set(str, strings.length);
            strings.push(btoa(str));
        }
        return `_0x${stringMap.get(str).toString(16)}`;
    });

    // 2. 生成字符串数组
    const stringArray = `var _0xstr = ${JSON.stringify(strings)};\n`;

    // 3. 生成解码函数
    const decoder = `
        var _0xdec = function(i) {
            return atob(_0xstr[i]);
        };
    `;

    // 4. 变量名混淆
    code = code.replace(/[a-zA-Z_$][a-zA-Z0-9_$]*/g, (match) => {
        if (match === 'console' || match === 'log') return match;
        return '_0x' + Math.random().toString(36).substr(2, 8);
    });

    return stringArray + decoder + code;
}

// 测试
const original = `console.log("Hello World");`;
console.log(simpleObfuscate(original));

console.log("Hello World");

// 混淆后
var _0x5b5a = ['SGVsbG8gV29ybGQ='];  // Base64("Hello World")
var _0x12345 = function(i) {
    return atob(_0x5b5a[i]);  // 运行时解码
};
console.log(   _0x12345(0)  );  // console.log()






// 原始代码
var a = 1;
var b = 2;
var c = a + b;
console.log("a=", a, "b=", b, "a+b=", c)
// 混淆后（简化版）
var state = 0;
while (true) {
    switch (state) {
        case 0:
            var a = 1;
            state = 1;
            continue;
        case 1:
            var b = 2;
            state = 2;
            continue;
        case 2:
            var c_ = a + b;
            state = 3;
            continue;
        case 3:
            break;
    }
    break;
}
console.log(c_)


// 死代码注入（Dead Code Injection）
// var _0x254b44 = function() {
//    var _0x320b8f = {};
//    _0x320b8f['SffFZ'] = _0x1d6c('0xa');
//    _0x320b8f[_0x1d6c('0x2c')] = 'INirR';  // 永远不会为真的条件
//    // ... 大量无用分支
// };



//console.log(map);
//{
//  '0': 'kbKmi',
//  '1': 'Pnwud',
//  '2': 'nAEHV',
//  '3': 'table',
//  '4': '^([^ ]+( +[^ ]+)+)+[^ ]}',
//  '5': '5|0|1|2|4|9|8|7|6|3',
//  '6': 'trunc',
//  '7': 'gsAja',
//  '8': 'iIbMP',
//  '9': 'AycTs',
//  '10': 'split',
//  '11': 'return (function() ',
//  '12': 'mRvHS',
//  '13': 'exception',
//  '14': 'innerText',
//  '15': 'info',
//  '16': 'KHcHd',
//  '17': 'XYzlX',
//  '18': 'test',
//  '19': 'ranking',
//  '20': 'lQDBm',
//  '21': 'WwoXn',
//  '22': 'passwd',
//  '23': 'MyhRp',
//  '24': 'insertRow',
//  '25': 'BRVYI',
//  '26': 'error',
//  '27': 'iMwEb',
//  '28': 'json',
//  '29': 'MdqlF',
//  '30': '1|2|7|4|6|0|5|3',
//  '31': 'YUqaF',
//  '32': 'apply',
//  '33': 'gzjlJ',
//  '34': 'debug',
//  '35': 'return /" + this + "/',
//  '36': 'BTZHf',
//  a: 'used_count',
//  b: 'time_to_crack_it',
//  c: 'trace',
//  d: 'log',
//  e: 'SffFZ',
//  f: 'lXONL',
//  '1a': 'dataContent',
//  '1b': 'EFYBs',
//  '1c': 'then',
//  '1d': 'getTime',
//  '1e': '0|3|2|1|5|7|6|4',
//  '1f': 'ttFat',
//  '2a': 'warn',
//  '2b': 'getElementById',
//  '2c': '4|3|5|0|2|7|8|1|6',
//  '2d': 'insertCell',
//  '2e': 'console',
//  '2f': 'forEach'
//}