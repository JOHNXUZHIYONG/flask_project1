var today = new Date(); //获取当前日期
var year = today.getFullYear(); //获取年份
var month = today.getMonth() + 1; //获取月份（0-11表示1-12月）
var date = today.getDate(); //获取日期
var firstDay = new Date(year, month - 1, 1).getDay(); //获取本月的第一天是星期几（0-6表示周日到周六）

function generateCalendar() {
    //找到日历表格和表格的tbody元素
    var table = document.querySelector('table');
    var tbody = table.querySelector('tbody');

    // 清除现有的tbody元素
    while (tbody.firstChild) {
        tbody.removeChild(tbody.firstChild);
    }

    // 添加单元格以显示日期
    var date = 1;
    for (var i = 0; i < 6; i++) {
        var row = document.createElement('tr');
        for (var j = 0; j < 7; j++) {
            var cell = document.createElement('td');
            if (i === 0 && j < firstDay) {
                //空白单元格填充日历表头
                var cellText = document.createTextNode('');
            } else if (date > daysInMonth(month, year)) {
                // 如果日期超过本月天数，填写空白单元格
                var cellText = document.createTextNode('');
            } else {
                // 填充日期
                var cellText = document.createTextNode(date);
                if (date === today.getDate() && year === today.getFullYear() && month === (today.getMonth() + 1)) {
                    cell.classList.add('today'); //为当前日期添加类的类名（ today）
                }
                date++;
            }
            cell.appendChild(cellText);
            row.appendChild(cell);
        }
        tbody.appendChild(row);
    }
}

function daysInMonth(month, year) {
    // 返回指定年份月份的天数
    return new Date(year, month, 0).getDate();
}

generateCalendar();
