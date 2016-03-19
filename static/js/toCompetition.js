var orgCount = 1;
var dayCount = 1;
var distCount = 1;
var duCount = 1;

function trPzClick(day_n){
    $('#PzState1'+day_n.toString()).toggle();
    $('#PzState2'+day_n.toString()).toggle();
};

function trTzClick(day_n){
    $('#TzState1'+day_n.toString()).toggle();
    $('#TzState2'+day_n.toString()).toggle();
};

$('.swapVisInfo').click(function(){
    var dayToSwap = $(this).val();
    var blockName = "#toSwapInfo" + dayToSwap.toString();
    var butImgUp = "#swapImgInfoUp" + dayToSwap.toString();
    var butImgDown = "#swapImgInfoDown" + dayToSwap.toString();
    $(butImgDown).toggle();
    $(butImgUp).toggle();
    $(blockName).slideToggle(400);
    componentHandler.upgradeAllRegistered();
});
$('.swapVisDiz').click(function(){
    var dayToSwap = $(this).val();
    var blockName = "#toSwapDiz" + dayToSwap.toString();
    var butImgUp = "#swapImgDizUp" + dayToSwap.toString();
    var butImgDown = "#swapImgDizDown" + dayToSwap.toString();
    $(butImgDown).toggle();
    $(butImgUp).toggle();
    $(blockName).slideToggle(400);
    componentHandler.upgradeAllRegistered();
});
$('#swapVisMem1').click(function(){
    var dayToSwap = $(this).val();
    var blockName = "#toSwapMem" + dayToSwap.toString();
    var butImgUp = "#swapImgMemUp" + dayToSwap.toString();
    var butImgDown = "#swapImgMemDown" + dayToSwap.toString();
    $(butImgDown).toggle();
    $(butImgUp).toggle();
    $(blockName).slideToggle(400);
    componentHandler.upgradeAllRegistered();
});


$('.addOrg').click(function(){
     var dayNum= $(this).siblings()[0].innerHTML;
     var grid = document.createElement('div');
     grid.className = 'mdl-grid';
     grid.style.margin = "-20px 0 20px 70px";
     grid.style.padding = '0 0 0 0';
     grid.style.height = '50px';
     grid.style.bottom = '20px';
     grid.style.width = '90%';
     grid.setAttribute('id', 'addOrgLine'+orgCount.toString());
     var col1 = document.createElement('div'); col1.className = 'mdl-cell--1-col';
     var col2 = document.createElement('div'); col2.className = 'mdl-cell--3-col';
        var textfield1 = document.createElement('div');
        textfield1.setAttribute('style', 'width: 100%; padding: 20px 0 20px 0;');
        textfield1.className = 'mdl-textfield mdl-js-textfield';
            var IdName = 'orgFio'+orgCount.toString()+dayCount.toString();
            var in1 = document.createElement('input');
            in1.className = 'mdl-textfield__input';
            in1.setAttribute('style', 'font-size: 16px;');
            in1.setAttribute('name', IdName);
            in1.setAttribute('id', IdName);
            var label1 = document.createElement('label');
            label1.className = 'mdl-textfield__label';
            label1.htmlFor = IdName;
            label1.innerHTML = "Введите ФИО";
        textfield1.appendChild(in1);
        textfield1.appendChild(label1);
     col2.appendChild(textfield1);
     var col3 = document.createElement('div'); col3.className = 'mdl-cell--1-col';
     var col4 = document.createElement('div'); col4.className = 'mdl-cell--3-col';
        var textfield2 = document.createElement('div');
        textfield2.setAttribute('style', 'width: 100%; padding:20px 0 20px 0;');
        textfield2.className = 'mdl-textfield mdl-js-textfield';
            var Dol = 'orgDol'+orgCount.toString()+dayCount.toString();
            var in2 = document.createElement('input');
            in2.className = 'mdl-textfield__input';
            in2.setAttribute('style', 'font-size: 16px;');
            in2.setAttribute('name', Dol);
            in2.setAttribute('id', Dol);
            var label2 = document.createElement('label');
            label2.className = 'mdl-textfield__label';
            label2.htmlFor = Dol;
            label2.innerHTML = "Введите должность";
        textfield2.appendChild(in2);
        textfield2.appendChild(label2);
     col4.appendChild(textfield2);
     var col5 = document.createElement('div'); col5.className = 'mdl-cell--1-col';
     var col6 = document.createElement('div'); col6.className = 'mdl-cell--3-col';
        var textfield3 = document.createElement('div');
        textfield3.setAttribute('style', 'width: 100%; padding: 20px 0 20px 0;');
        textfield3.className = 'mdl-textfield mdl-js-textfield';
            var Cont = 'orgCont'+orgCount.toString()+dayCount.toString();
            var in3 = document.createElement('input');
            in3.className = 'mdl-textfield__input';
            in3.setAttribute('style', 'font-size: 16px;');
            in3.setAttribute('name', Cont);
            in3.setAttribute('id', Cont);
            var label3 = document.createElement('label');
            label3.className = 'mdl-textfield__label';
            label3.htmlFor = Cont;
            label3.innerHTML = "Введите контакт";
        textfield3.appendChild(in3);
        textfield3.appendChild(label3);
     col6.appendChild(textfield3);
     grid.appendChild(col1);
     grid.appendChild(col2);
     grid.appendChild(col3);
     grid.appendChild(col4);
     grid.appendChild(col5);
     grid.appendChild(col6);
     var addButtonDiv = document.getElementById('addOrgInsert'+dayNum.toString());
     var blockInsert = addButtonDiv.parentNode;
     blockInsert.insertBefore(grid, addButtonDiv);
     orgCount = orgCount+1;
     componentHandler.upgradeAllRegistered();                 

    /*   $.ajax({
             type: "POST",
             data: {'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(), 'old_paper': oldPaperCount},
             url: "/add_paper/",
         });        */ 
});

$("#addGroupDiz").click(function(){    
    var grid = document.createElement('div');
    grid.className = 'mdl-grid';
    grid.style.margin = "-20px 0 20px 0";
    grid.style.padding = '0 0 0 0';
    grid.style.height = '50px';
    grid.style.bottom = '20px';
    grid.setAttribute('id', 'addGroupLine'+distCount.toString());
    var col1 = document.createElement('div'); col1.className = 'mdl-cell--2-col';
    var col2 = document.createElement('div'); col2.className = 'mdl-cell--1-col';
        var textfield1 = document.createElement('div');
        textfield1.setAttribute('style', 'width: 110%; max-width: 110%; padding: 20px 0 20px 0;');
        textfield1.className = 'mdl-textfield mdl-js-textfield';
            var IdName = 'dizGroup'+distCount.toString()+dayCount.toString();
            var in1 = document.createElement('input');
            in1.className = 'mdl-textfield__input';
            in1.setAttribute('style', 'font-size: 16px;');
            in1.setAttribute('name', IdName);
            in1.setAttribute('id', IdName);
            var label1 = document.createElement('label');
            label1.className = 'mdl-textfield__label';
            label1.htmlFor = IdName;
            label1.innerHTML = "Группа";
        textfield1.appendChild(in1);
        textfield1.appendChild(label1);
     col2.appendChild(textfield1);
    var col3 = document.createElement('div'); col3.className = 'mdl-cell--1-col';
    var col4 = document.createElement('div'); col4.className = 'mdl-cell--1-col';
        var textfield2 = document.createElement('div');
        textfield2.setAttribute('style', 'width: 120%; max-width: 120%; padding: 20px 0 20px 0;');
        textfield2.className = 'mdl-textfield mdl-js-textfield';
            IdName = 'dizLen'+distCount.toString()+dayCount.toString();
            var in2 = document.createElement('input');
            in2.className = 'mdl-textfield__input';
            in2.setAttribute('style', 'font-size: 16px;');
            in2.setAttribute('name', IdName);
            in2.setAttribute('id', IdName);
            var label2 = document.createElement('label');
            label2.className = 'mdl-textfield__label';
            label2.htmlFor = IdName;
            label2.innerHTML = "Длина";
        textfield2.appendChild(in2);
        textfield2.appendChild(label2);
     col4.appendChild(textfield2);
    var col5 = document.createElement('div'); col5.className = 'mdl-cell--1-col';
        var textfield3 = document.createElement('div');
        textfield3.setAttribute('style', 'width: 120%; max-width: 120%; padding: 20px 0 20px 0; left: 40px;');
        textfield3.className = 'mdl-textfield mdl-js-textfield';
            IdName = 'dizClass'+distCount.toString()+dayCount.toString();
            var in3 = document.createElement('input');
            in3.className = 'mdl-textfield__input';
            in3.setAttribute('style', 'font-size: 16px;');
            in3.setAttribute('name', IdName);
            in3.setAttribute('id', IdName);
            var label3 = document.createElement('label');
            label3.className = 'mdl-textfield__label';
            label3.htmlFor = IdName;
            label3.innerHTML = "Класс";
        textfield3.appendChild(in3);
        textfield3.appendChild(label3);
     col5.appendChild(textfield3);
    var col6 = document.createElement('div'); col6.className = 'mdl-cell--5-col';
    col6.setAttribute('style', 'text-align: center;'); 
        var textfield4 = document.createElement('div');
        textfield4.setAttribute('style', 'width: 40px; padding: 20px 0 20px 0;');
        textfield4.className = 'mdl-textfield mdl-js-textfield';
            IdName = 'dizCCmin'+distCount.toString()+dayCount.toString();
            var in4 = document.createElement('input');
            in4.className = 'mdl-textfield__input';
            in4.setAttribute('style', 'font-size: 16px;');
            in4.setAttribute('name', IdName);
            in4.setAttribute('id', IdName);
            var label4 = document.createElement('label');
            label4.className = 'mdl-textfield__label';
            label4.htmlFor = IdName;
            label4.innerHTML = "min";
        textfield4.appendChild(in4);
        textfield4.appendChild(label4);
        var textfield5 = document.createElement('div');
        textfield5.setAttribute('style', 'width: 40px; padding: 20px 0 20px 0;');
        textfield5.className = 'mdl-textfield mdl-js-textfield';
            IdName = 'dizCCmax'+distCount.toString()+dayCount.toString();
            var in5 = document.createElement('input');
            in5.className = 'mdl-textfield__input';
            in5.setAttribute('style', 'font-size: 16px;');
            in5.setAttribute('name', IdName);
            in5.setAttribute('id', IdName);
            var label5 = document.createElement('label');
            label5.className = 'mdl-textfield__label';
            label5.htmlFor = IdName;
            label5.innerHTML = "max";
        var tire = document.createElement('span');
        tire.className = 'myP';
        tire.innerHTML = ' - ';
        textfield5.appendChild(in5);
        textfield5.appendChild(label5);
     col6.appendChild(textfield4);
     col6.appendChild(tire);
     col6.appendChild(textfield5);
    var col7 = document.createElement('div'); col7.className = 'mdl-cell--1-col';
    grid.appendChild(col1);
    grid.appendChild(col2);
    grid.appendChild(col3);
    grid.appendChild(col4);
    grid.appendChild(col5);
    grid.appendChild(col6);
    grid.appendChild(col7);
    var addButtonDiv = document.getElementById('addGroupInsert');
    var blockInsert = addButtonDiv.parentNode;
    blockInsert.insertBefore(grid, addButtonDiv);
    componentHandler.upgradeAllRegistered();
    distCount = distCount + 1;
});


$("#addMemDiz").click(function(){
    var grid = document.createElement('div');
    grid.className = 'mdl-grid';
    grid.style.margin = "-20px 0 20px 0";
    grid.style.padding = '0 0 0 0';
    grid.style.height = '50px';
    grid.style.bottom = '20px';
    grid.style.textAlign = 'center';
    grid.setAttribute('id', 'addDistLine'+duCount.toString());
    var col1 = document.createElement('div'); col1.className = 'mdl-cell--2-col';
    var col2 = document.createElement('div'); col2.className = 'mdl-cell--1-col';
        var textfield1 = document.createElement('div');
        textfield1.setAttribute('style', 'width: 110%; max-width: 110%; padding: 20px 0 20px 0;');
        textfield1.className = 'mdl-textfield mdl-js-textfield';
            var IdName = 'duGroup'+duCount.toString()+dayCount.toString();
            var in1 = document.createElement('input');
            in1.className = 'mdl-textfield__input';
            in1.setAttribute('style', 'font-size: 16px;');
            in1.setAttribute('name', IdName);
            in1.setAttribute('id', IdName);
            var label1 = document.createElement('label');
            label1.className = 'mdl-textfield__label';
            label1.htmlFor = IdName;
            label1.innerHTML = "Группа";
        textfield1.appendChild(in1);
        textfield1.appendChild(label1);
     col2.appendChild(textfield1);
    var col3 = document.createElement('div'); col3.className = 'mdl-cell--1-col';
    var col4 = document.createElement('div'); col4.className = 'mdl-cell--1-col';
        var textfield2 = document.createElement('div');
        textfield2.setAttribute('style', 'width: 70%; padding: 20px 0 20px 0;');
        textfield2.className = 'mdl-textfield mdl-js-textfield';
            IdName = 'duSalary'+duCount.toString()+dayCount.toString();
            var in2 = document.createElement('input');
            in2.className = 'mdl-textfield__input';
            in2.setAttribute('style', 'font-size: 16px;');
            in2.setAttribute('name', IdName);
            in2.setAttribute('id', IdName);
            var label2 = document.createElement('label');
            label2.className = 'mdl-textfield__label';
            label2.htmlFor = IdName;
            label2.innerHTML = "Стартовый";
        textfield2.appendChild(in2);
        textfield2.appendChild(label2);
     col4.appendChild(textfield2);
    var col5 = document.createElement('div'); col5.className = 'mdl-cell--1-col';
    var col6 = document.createElement('div'); col6.className = 'mdl-cell--2-col';
        var textfield3 = document.createElement('div');
        textfield3.setAttribute('style', 'width: 40px; padding: 20px 0 20px 0;');
        textfield3.className = 'mdl-textfield mdl-js-textfield';
            IdName = 'duAgemin'+duCount.toString()+dayCount.toString();
            var in3 = document.createElement('input');
            in3.className = 'mdl-textfield__input';
            in3.setAttribute('style', 'font-size: 16px;');
            in3.setAttribute('name', IdName);
            in3.setAttribute('id', IdName);
            var label3 = document.createElement('label');
            label3.className = 'mdl-textfield__label';
            label3.htmlFor = IdName;
            label3.innerHTML = "min";
        textfield3.appendChild(in3);
        textfield3.appendChild(label3);
        var textfield4 = document.createElement('div');
        textfield4.setAttribute('style', 'width: 40px; padding: 20px 0 20px 0;');
        textfield4.className = 'mdl-textfield mdl-js-textfield';
            IdName = 'duAgemax'+duCount.toString()+dayCount.toString();
            var in4 = document.createElement('input');
            in4.className = 'mdl-textfield__input';
            in4.setAttribute('style', 'font-size: 16px;');
            in4.setAttribute('name', IdName);
            in4.setAttribute('id', IdName);
            var label4 = document.createElement('label');
            label4.className = 'mdl-textfield__label';
            label4.htmlFor = IdName;
            label4.innerHTML = "max";
        textfield4.appendChild(in4);
        textfield4.appendChild(label4);
        var tire = document.createElement('span');
        tire.className = 'myP';
        tire.innerHTML = ' - ';
     col6.appendChild(textfield3);
     col6.appendChild(tire);
     col6.appendChild(textfield4);
    var col7 = document.createElement('div'); col7.className = 'mdl-cell--1-col';
    var col8 = document.createElement('div'); col8.className = 'mdl-cell--2-col';
        var textfield5 = document.createElement('div');
        textfield5.setAttribute('style', 'width: 40px; padding: 20px 0 20px 0;');
        textfield5.className = 'mdl-textfield mdl-js-textfield';
            IdName = 'duQualmin'+duCount.toString()+dayCount.toString();
            var in5 = document.createElement('input');
            in5.className = 'mdl-textfield__input';
            in5.setAttribute('style', 'font-size: 16px;');
            in5.setAttribute('name', IdName);
            in5.setAttribute('id', IdName);
            var label5 = document.createElement('label');
            label5.className = 'mdl-textfield__label';
            label5.htmlFor = IdName;
            label5.innerHTML = "min";
        textfield5.appendChild(in5);
        textfield5.appendChild(label5);
        var textfield6 = document.createElement('div');
        textfield6.setAttribute('style', 'width: 40px; padding: 20px 0 20px 0;');
        textfield6.className = 'mdl-textfield mdl-js-textfield';
            IdName = 'duQualmax'+duCount.toString()+dayCount.toString();
            var in6 = document.createElement('input');
            in6.className = 'mdl-textfield__input';
            in6.setAttribute('style', 'font-size: 16px;');
            in6.setAttribute('name', IdName);
            in6.setAttribute('id', IdName);
            var label6 = document.createElement('label');
            label6.className = 'mdl-textfield__label';
            label6.htmlFor = IdName;
            label6.innerHTML = "max";
        textfield6.appendChild(in6);
        textfield6.appendChild(label6);
        var tire2 = document.createElement('span');
        tire2.className = 'myP';
        tire2.innerHTML = ' - ';
     col8.appendChild(textfield5);
     col8.appendChild(tire2);
     col8.appendChild(textfield6);
    var col9 = document.createElement('div'); col9.className = 'mdl-cell--1-col';        
    grid.appendChild(col1);
    grid.appendChild(col2);
    grid.appendChild(col3);
    grid.appendChild(col4);
    grid.appendChild(col5);
    grid.appendChild(col6);
    grid.appendChild(col7);
    grid.appendChild(col8);
    grid.appendChild(col9);
    var addButtonDiv = document.getElementById('addMemDizInsert');
    var blockInsert = addButtonDiv.parentNode;
    blockInsert.insertBefore(grid, addButtonDiv);
    componentHandler.upgradeAllRegistered();
    duCount = duCount + 1;
});