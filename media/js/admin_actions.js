function getObjFromJson(json) {
			return jQuery.parseJSON(json);
}

function remUser(uid) {
	if (confirm("Are you sure?")) {
				$.ajax({ 
					url: "/admin/rem_user/",
					type: "POST",
					data: 'user_id=' + uid,
					success: function(response){
						if (getObjFromJson(response).success) {
							var target = '#user-row-' + uid;
							$(target).fadeOut(500, function(target){
								$(target).remove();
							});
						} else {
							alert('Oops!');
						}
      				},
      			});
	}
	return false;
}
