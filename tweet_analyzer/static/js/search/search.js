

var SearchTwitter = (function(){
	function sendSearch(isExport){
		if ($('#searchq').val().length == 0)
		{
			$('#errorMessage').removeClass("d-none");
		}
		else
		{
			$('#errorMessage').addClass("d-none");
			$('#returnedJson').val('');
			var mainUrl  = getMainUrl();
			if (isExport){
				mainUrl = mainUrl + '&isExport=True';
				location.replace(mainUrl);
				$('#returnedJson').html('');
			}
			else {
			$.getJSON(mainUrl, {})
				.done(function(data){
					$('#returnedJson').html(JSON.stringify(data));
				})
				.fail(function( jqxhr, textStatus, error ) {
				    var err = textStatus + ", " + error;
				    $('#returnedJson').html(jqxhr.responseText);
				});
			}
		}
	}


	function getMainUrl(){
		$('#errorMessage').addClass("hide");
		var mainUrl = 'get_tweets?searchq=' + encodeURI($('#searchq').val());
		if ($('#searchFromDate').val())
		{
			formattedsearchFromDate = $('#searchFromDate').val();
			mainUrl = mainUrl + "&fromDate=" + encodeURI(formattedsearchFromDate);
		}
		if ($('#searchToDate').val())
		{
			var formattedsearchToDate = $('#searchToDate').val();
			mainUrl = mainUrl + "&toDate=" + encodeURI(formattedsearchToDate);
		}
		$('#returnedJson').html("Getting twitter data...");

		return mainUrl;

	}

	function format_date(formatDate){
		formatDate = new Date(formatDate);
		var dateString = '';
		dateString = dateString.concat(formatDate.getFullYear().toString());
		var month = formatDate.getMonth() + 1;
		if (month.toString().length < 2)
			dateString = dateString.concat("0");
		dateString = dateString.concat(month.toString());
		if (formatDate.getDate().toString().length < 2)
			dateString = dateString.concat("0");
		dateString = dateString.concat(formatDate.getDate().toString());
		if (formatDate.getHours().toString().length < 2)
			dateString = dateString.concat("0");
		dateString = dateString.concat(formatDate.getHours().toString());
		if (formatDate.getMinutes().toString().length < 2)
			dateString = dateString.concat("0");
		dateString = dateString.concat(formatDate.getMinutes().toString());
		return dateString;
	}

	// return public functions
	return {
		search : sendSearch
	};
})();
