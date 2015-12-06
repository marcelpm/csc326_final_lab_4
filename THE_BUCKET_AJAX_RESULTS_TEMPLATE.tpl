%if results != None:

	% for result in results:

	<div class="result_div">
		<a href="{{result['url']}}">{{result['title']}}</a><br>
		<cite>{{result['url']}}</cite><br>
		<span>{{result['text']}}</span>
	</div>

	% end

%end