<!DOCTYPE html>
<html>
<head>
	<title></title>
	<script type="text/javascript" >
		var results_div = null;
		var text_input = null;


		window.onload = function(){

			results_div = document.getElementById('all_results_div');
			text_input = document.getElementById('query_string');


			text_input.addEventListener('input', function(){
				input_changed_handler();
			});
		}





		var input_changed_timeout = null;

		var input_changed_handler = function() {

			clearTimeout(input_changed_timeout);
			input_changed_timeout = setTimeout(input_changed_timeout_function, 500);
		};

		var input_changed_timeout_function = function() {

			var ajax_object = new send_ajax_query_object();
			
			ajax_object.Send_Query(text_input.value);


		}

		var ajax_increment = 0;


		var highest_received_increment = -1;

		var send_ajax_query_object = function() {
			//get the current increment so as not so display the wrong one if a packet is received out-of-order, always displaying most recent query
			
			var this_ajax_increment = ajax_increment;

			ajax_increment++;
			
			var xhttp = new XMLHttpRequest();

			this.Send_Query = function(query_string1) {
				
				//window.alert(query_string1);
				xhttp.onreadystatechange = function(){

					if(xhttp.readyState == 4 && xhttp.status == 200) {

						//window.alert(highest_received_increment);
						if(this_ajax_increment >=  highest_received_increment){

							highest_received_increment = this_ajax_increment;

							// while(results_div.firstChild) {
							// 	results_div.removeChild(results_div.firstChild);
							// }
							//SHOULD DEFINATELY FIX THE POSSIBLE MEMORY LEAK SETTING INNERHTML


							results_div.innerHTML = xhttp.responseText;	
						}

					}
				}
				xhttp.open("GET", "/home/ajax_query?query_string="+query_string1, true);
				xhttp.send();

			}
			
		}
	</script>
	<style>
		.my-icon {
		    position: relative;
		}
		.my-icon > i {
		    position: absolute;
		    display: inline-block;
		    width: 0;
		    height: 0;
		    line-height: 0;
		    border: 1.5em solid #4a608c;
		    border-bottom: 1.5em solid #4a608c;
		    left: 0em;
		    top: 0em;
		}
		.my-icon > i+i {
		    position: absolute;
		    display: inline-block;
		    width: 0;
		    height: 0;
		    line-height: 0;
		    border: 1.5em solid #1142AA;
		    border-top: none;
		    border-bottom-right-radius: 1.5em;
		    border-bottom-left-radius: 1.5em;
		    left: 0em;
		    top: 0em;
		}
		.my-icon > i+i+i {
		    position: absolute;
		    display: inline-block;
		    width: 0;
		    height: 0;
		    line-height: 0;
		    border: 1.5em solid #d9e1f1;
		    border-top: none;
		    border-bottom-right-radius: 1.5em;
		    border-bottom-left-radius: 1.5em;
		    left: 0em;
		    top: 0em;
		}
		div.result_div {
			border-width: 2px;
			border-style: solid;
			border-color: white;
			padding-top: 10px;
			padding-bottom: 10px;
		}
	</style>

</head>
<body style="background-color:black;color:white">
	<div style="height:200px">
		
		<div style="float:right">
		<div id="login_stuffs">
			sign in from <a href="/login">HERE</a>
		</div>
		</div>
		
	</div>
	<div id="center_div" align="center">
		<a href="/">
			<i class="my-icon" style="margin-right:65%;float:right"><i></i><i></i><i></i></i>
			<text style="font-size:50px;font-weight:bold;color:lightblue;margin-left:40%;float:left">
				The Bucket
			</text>
		</a>
		
		<div style="position:relative;clear:both;">
			<div align="center">
				<form name="query_form" method="get" action="/home/query">
					<input type="text" name="query_string" id="query_string"></input>
					<input type="submit" name="submit_button" value="Submit"></input>
				</form>
			</div>
		</div>

		%if errors != None:
			%for err in errors:
			<div>{{err}}</div>
			%end
		%end

		%if autocorrect != None:
		<div> 
			Did you mean: 
			<a href="/home/query?query_string={{autocorrect}}"> {{autocorrect}}</a> 
		</div>
		%end

		%if query_string != None:
		<div> Currently showing results for: {{query_string}}</div>
		%end

		%if nav_info != None:
		<div id="nav_bar_top_div">

			<table align="center">
				<tr>
					%if 'previous_page_url' in nav_info:
					<td>
						<a href="{{nav_info['previous_page_url']}}" style="">PREVIOUS</a>
					</td>
					%end
					%if 'current_page' in nav_info:
					<td>
						<div id="current_page_div" style="color:white">CURRENT PAGE: {{nav_info['current_page'] + 1}} of {{nav_info['number_of_pages']}}</div>
					</td>
					%end
					%if 'next_page_url' in nav_info:
					<td>
						<a style="" href="{{nav_info['next_page_url']}}">NEXT</a>
					</td>
					%end
				</tr>
			</table>

		</div>
		%end

		
		<div id="all_results_div" align="left" style="margin-left:30%;float:left;width:50%">
		%if results != None:
			% for result in results:

			<div class="result_div">
				<a href="{{result['url']}}">{{result['title']}}</a><br>
				<cite>{{result['url']}}</cite><br>
				<span>{{result['text']}}</span>
			</div>

			% end
		%end
		</div>
		

		%if nav_info != None:
		<div id="nav_bar_bottom_div" style="position:relative;clear:both">

			<table align="center">
				<tr>
					%if 'previous_page_url' in nav_info:
					<td>
						<a href="{{nav_info['previous_page_url']}}" style="">PREVIOUS</a>
					</td>
					%end
					%if 'current_page' in nav_info:
					<td>
						<div id="current_page_div" style="color:white">CURRENT PAGE: {{nav_info['current_page'] + 1}} of {{nav_info['number_of_pages']}}</div>
					</td>
					%end
					%if 'next_page_url' in nav_info:
					<td>
						<a style="" href="{{nav_info['next_page_url']}}">NEXT</a>
					</td>
					%end
				</tr>
			</table>

		</div>
		%end
	</div>
</body>
</html>