//Organizer
$('#addOrgan').click(function(){
    $('#sectB').toggle();
	$('#sect0').toggle();
    $('#sect1').toggle();
	$('#formAddOrg').toggle();
});
$('#addOrgBack').click(function(){
    $('#sectB').toggle();
	$('#sect0').toggle();
    $('#sect1').toggle();
	$('#formAddOrg').toggle();
});

$('.changeOrgan').click(function(){
	var cols = $(this).parent().parent().siblings();
	var fio = $('#olFio');
	fio.val(cols[0].innerHTML);
    fio.parent().addClass('is-dirty');
	var cont = $('#olContact');
    cont.val(cols[1].innerHTML);
    cont.parent().addClass('is-dirty');
	$('#olKey').val($(this).siblings()[1].value);
	$("#sectB").toggle();
	$('#sect1').toggle();
	$('#sect2').toggle();
});
$('#changeOrgBack').click(function(){
    $('#sectB').toggle();
	$('#sect1').toggle();
    $('#sect2').toggle();
});

//Member
$('#addMemb').click(function(){
	$('#sectB').toggle();
	$('#sect0').toggle();
    $('#formNewMember').toggle();
	$('#formAddMember').toggle();
});
$('#addMemBack').click(function(){
	$('#sectB').toggle();
	$('#sect0').toggle();
    $('#formNewMember').toggle();
	$('#formAddMember').toggle();
});

$('.changeMemb').click(function(){
	var cols = $(this).parent().parent().siblings();
	var fio = $('#omFio');
	fio.val(cols[0].innerHTML);
    fio.parent().addClass('is-dirty');
	var gr = $('#omGr');
	gr.val(cols[1].innerHTML);
    gr.parent().addClass('is-dirty');
	var qual = $('#omRazr');
	qual.val(cols[2].innerHTML);
    qual.parent().addClass('is-dirty');
	var comm = $('#omComand');
	comm.val(cols[3].innerHTML);
    comm.parent().addClass('is-dirty');
	var terr = $('#omTerritory');
	terr.val(cols[4].innerHTML);
    terr.parent().addClass('is-dirty');
	$('#omKey').val($(this).siblings()[1].value);
	$('#sectB').toggle();
	$('#formNewMember').toggle();
	$('#sect2').toggle();
});
$('#changeMemBack').click(function(){
	$('#sectB').toggle();
	$('#formNewMember').toggle();
	$('#sect2').toggle();
});

//Leader
$('#addLeader').click(function(){
	$('#sectB').toggle();
	$('#sect0').toggle();
    $('#formNewLeader').toggle();
	$('#formAddLeader').toggle();
});
$('#addLeaderBack').click(function(){
	$('#sectB').toggle();
	$('#sect0').toggle();
    $('#formNewLeader').toggle();
	$('#formAddLeader').toggle();
});

$('.changeLeader').click(function(){
	var cols = $(this).parent().parent().siblings();
	var fio = $('#llFio');
    fio.val(cols[0].innerHTML);
    fio.parent().addClass('is-dirty');
	var comm = $('#llComand');
    comm.val(cols[1].innerHTML);
    comm.parent().addClass('is-dirty');
	var terr = $('#llTerritory');
    terr.val(cols[2].innerHTML);
    terr.parent().addClass('is-dirty');
	var cont = $('#llContact');
    cont.val(cols[3].innerHTML);
    cont.parent().addClass('is-dirty');
    $('#llKey').val($(this).siblings()[1].value);
	$('#sectB').toggle();
    $('#formNewLeader').toggle();
	$('#sect2').toggle();
});

$('#changeLeaderBack').click(function(){
	$('#sectB').toggle();
	$('#formNewLeader').toggle();
	$('#sect2').toggle();
});

$('#deleteLeader').click(function(){
	//AJAX удаление рукля
	$('#sovText').text('Руководитель ВАСИЛИЙ ГУЗЕЕВ удален из базы');
	$('#sovDiv').fadeIn(100);
	setTimeout("$('#sovDiv').fadeOut();", 2000);
});