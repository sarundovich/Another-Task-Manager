		$(document).ready(function() {
    		$('#new-task-btn').click(showNewTaskForm);
			$('#new-task-cancel').click(hideNewTaskForm);
			$('#new-task-submit').click(addNewTask);
			$('#deadline').datepicker({ dateFormat: $.datepicker.W3C });
			$('.edit').editable('/tasks/edit/', {
				cssclass: 'editable',
				cancel: 'Cancel',
				width: '100%',
				submit: 'Save',
         		indicator: '<img src="/static/img/ajax-loader.gif">',
         		tooltip: 'Click to edit your task'
			});
		});
		
		function showNewTaskForm() {
			$('#new-task-btn').hide();
			$('#new-task').show();
		}
		
		function hideNewTaskForm() {
			$('#new-task').hide();
			clearInputs();
			$('#new-task-btn').show();
		}
		
		function clearInputs() {
			$('#deadline').val('');
			$('#name').val('');
			$('#new-task-msg').empty();
			$('#priority').attr('checked', false);
		}
		
		function getObjFromJson(json) {
			return jQuery.parseJSON(json);
		}
		
		function addNewTask() {
			var deadline = $('#deadline').val();
			var name = $('#name').val();
			var hi_prior = $('#priority').attr('checked');
			if (deadline == '' || name == '') {
				$('#new-task-msg').empty().append('<span class=\'hint\'>Hint: Try to fill all of the fields below</span>').show();
			} else {
				$('#new-task-msg').empty();
				var request_data = 'deadline=' + deadline + '&name=' + name + '&is_hi_prior=' + hi_prior;
				$.ajax({ 
					url: "/ajax/add_task/",
					type: "POST",
					data: request_data,
					complete: function() {
						$('#ajax-indicator').hide();
					},
					success: function(response) {
						response = getObjFromJson(response);
						if (response.success) {
							renderTaskById(response.task_id);
						} else {
							alert('Oops!');
						}
        				hideNewTaskForm();
      				},
      				beforeSend: function() {
      					$('#ajax-indicator').show();
      				}
      			});
			}
			return false;
		}
		
		function renderTaskById(task_id) {
			data = 'task_id=' + task_id
			$.get('/ajax/render_task/', data, function(resp) {
				resp = getObjFromJson(resp);
				if (resp.success) {
  					$('#tasks-holder').append(resp.task_html);
  				} else {
  					alert('Oops!');
  				}
			});
		}
		
		function removeTask(task_id) {
			if (confirm("Are you sure?")) {
				$.ajax({ 
					url: "/ajax/rem_task/",
					type: "POST",
					data: 'task_id=' + task_id,
					success: function(response){
						if (getObjFromJson(response).success) {
							var target = '#task-' + task_id;
							$(target).fadeOut(500, function(target){
								$(target).remove();
							});
						} else {
							alert('Oops!');
						}
      				},
      			});
			} else {
				return false;
			}
			return false;
		}
		
		function finishTask(task_id) {
			$.ajax({ 
					url: "/ajax/finish_task/",
					type: "POST",
					data: 'task_id=' + task_id,
					success: function(response){
							resp = getObjFromJson(response)
						if (resp.success) {
							if (resp.is_done) {
								var a_lbl = 'Unfinish';
								$('#task-done-img-' + task_id).fadeIn(500);
								$('#task-text-' + task_id).css({'text-decoration': 'line-through'});
							} else {
								var a_lbl = 'Finish';
								$('#task-done-img-' + task_id).fadeOut(500);
								$('#task-text-' + task_id).css({'text-decoration': 'none'});
							}
							
							
							$('#finish-action-' + task_id).text(a_lbl)
							
						} else {
							alert('Oops!');
						}
      				},
      			});
      		return false;
		}
		
		function updateTaskList() {
			$.ajax({ 
					url: "/ajax/get_tasks/",
					type: "GET",
					success: function(response){
						data = getObjFromJson(response);
						if (data.success) {
							$('#tasks-holder').empty().append(data.tasks);
						} else {
							alert('Oops!');
						}
      				},
      		});
      		return false;
		}
