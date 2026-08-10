const encryptedData = "ewogICAgICAiZmxpZ2h0cyI6IFsKICAgICAgICB7ICJmcm9tIjogIuW5v+W3niIsICJ0byI6ICLljJfkuqwiLCAicHJpY2UiOiA4MDAgfSwKICAgICAgICB7ICJmcm9tIjogIuW5v+W3niIsICJ0byI6ICLkuIrmtbciLCAicHJpY2UiOiA3NTAgfSwKICAgICAgICB7ICJmcm9tIjogIuW5v+W3niIsICJ0byI6ICLmiJDpg70iLCAicHJpY2UiOiA3MDAgfSwKICAgICAgICB7ICJmcm9tIjogIuW5v+W3niIsICJ0byI6ICLmt7HlnLMiLCAicHJpY2UiOiAyMDAgfSwKICAgICAgICB7ICJmcm9tIjogIuW5v+W3niIsICJ0byI6ICLmna3lt54iLCAicHJpY2UiOiA2NTAgfSwKICAgICAgICB7ICJmcm9tIjogIuW5v+W3niIsICJ0byI6ICLljZfkuqwiLCAicHJpY2UiOiA2MDAgfSwKICAgICAgICB7ICJmcm9tIjogIuW5v+W3niIsICJ0byI6ICLph43luoYiLCAicHJpY2UiOiA3MjAgfSwKICAgICAgICB7ICJmcm9tIjogIuW5v+W3niIsICJ0byI6ICLopb/lrokiLCAicHJpY2UiOiA2ODAgfSwKICAgICAgICB7ICJmcm9tIjogIuW5v+W3niIsICJ0byI6ICLmmIbmmI4iLCAicHJpY2UiOiA2MjAgfSwKICAgICAgICB7ICJmcm9tIjogIuW5v+W3niIsICJ0byI6ICLmrabmsYkiLCAicHJpY2UiOiA1MDAgfSwKICAgICAgICB7ICJmcm9tIjogIuW5v+W3niIsICJ0byI6ICLplb/mspkiLCAicHJpY2UiOiA0ODAgfSwKICAgICAgICB7ICJmcm9tIjogIuW5v+W3niIsICJ0byI6ICLljqbpl6giLCAicHJpY2UiOiA0NTAgfSwKICAgICAgICB7ICJmcm9tIjogIuW5v+W3niIsICJ0byI6ICLpnZLlspsiLCAicHJpY2UiOiA3ODAgfSwKICAgICAgICB7ICJmcm9tIjogIuW5v+W3niIsICJ0byI6ICLlpKnmtKUiLCAicHJpY2UiOiA3MDAgfSwKICAgICAgICB7ICJmcm9tIjogIuW5v+W3niIsICJ0byI6ICLmsojpmLMiLCAicHJpY2UiOiA4NTAgfSwKICAgICAgICB7ICJmcm9tIjogIuW5v+W3niIsICJ0byI6ICLlpKfov54iLCAicHJpY2UiOiA4MzAgfSwKICAgICAgICB7ICJmcm9tIjogIuW5v+W3niIsICJ0byI6ICLlk4jlsJTmu6giLCAicHJpY2UiOiA5MDAgfSwKICAgICAgICB7ICJmcm9tIjogIuW5v+W3niIsICJ0byI6ICLkuInkupoiLCAicHJpY2UiOiA1NTAgfSwKICAgICAgICB7ICJmcm9tIjogIuW5v+W3niIsICJ0byI6ICLnj6DmtbciLCAicHJpY2UiOiAxODAgfSwKICAgICAgICB7ICJmcm9tIjogIuW5v+W3niIsICJ0byI6ICLmoYLmnpciLCAicHJpY2UiOiA0MDAgfQogICAgICBdCiAgICB9";

// 解`密`数据  就是base64编码
const flightData = JSON.parse(decodeURIComponent(atob(encryptedData).split('').map(c => '%' + c.charCodeAt(0).toString(16).padStart(2, '0')).join('')));
console.log(flightData)
//// 渲染表格
//const tableBody = document.querySelector('#flightTable tbody');
//flightData.flights.forEach(flight => {
//    const row = document.createElement('tr');
//    row.innerHTML = `
//        <td>${flight.from}</td>
//        <td>${flight.to}</td>
//        <td>${flight.price}</td>`;
//    tableBody.appendChild(row);
//});

{
  flights: [
    { from: '广州', to: '北京', price: 800 },
    { from: '广州', to: '上海', price: 750 },
    { from: '广州', to: '成都', price: 700 },
    { from: '广州', to: '深圳', price: 200 },
    { from: '广州', to: '杭州', price: 650 },
    { from: '广州', to: '南京', price: 600 },
    { from: '广州', to: '重庆', price: 720 },
    { from: '广州', to: '西安', price: 680 },
    { from: '广州', to: '昆明', price: 620 },
    { from: '广州', to: '武汉', price: 500 },
    { from: '广州', to: '长沙', price: 480 },
    { from: '广州', to: '厦门', price: 450 },
    { from: '广州', to: '青岛', price: 780 },
    { from: '广州', to: '天津', price: 700 },
    { from: '广州', to: '沈阳', price: 850 },
    { from: '广州', to: '大连', price: 830 },
    { from: '广州', to: '哈尔滨', price: 900 },
    { from: '广州', to: '三亚', price: 550 },
    { from: '广州', to: '珠海', price: 180 },
    { from: '广州', to: '桂林', price: 400 }
  ]
}