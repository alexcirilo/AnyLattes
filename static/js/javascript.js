$(document).ready(function(){			
    setTimeout(function() {
	$(".alert").fadeOut("slow", function(){
		$(this).alert('close');
	});				
    }, 500);			
});