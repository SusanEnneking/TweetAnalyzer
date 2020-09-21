

var SearchTwitter = (function(){
	function sendSearch(){
		if ($('#searchq').val().length == 0 
			|| $('#maxrequestcount').val().length == 0 
			|| $('#maxrequestcount').val() > 10
			|| $('#maxrequestcount').val() < 1
			)
		{
			$('#errorMessage').removeClass("d-none");
		}
		else
		{
			$('#errorMessage').addClass("d-none");
			$('#returnedJson').val('');
			var melData = getMainUrl();
			$.getJSON(melData, {})
				.done(function(data){
					$('#returnedJson').html(JSON.stringify(data));
				})
				.fail(function( jqxhr, textStatus, error ) {
				    var err = textStatus + ", " + error;
				    $('#returnedJson').html(jqxhr.ResponseText);
				});
		}
	}

	function sendExport(){
		if ($('#searchq').val().length == 0 || $('#maxrequestcount').val().length == 0)
		{
			$('#errorMessage').removeClass("hide");
		}
		else
		{
			var melData = getMainUrl() + '&isExport=True';
			download(melData, "key", "data");
		}
	}

	function download(url, key, data){
	    // Build a form
	    var form = $('<form></form>').attr('action', url).attr('method', 'post');
	    // Add the one key/value
	    form.append($("<input></input>").attr('type', 'hidden').attr('name', key).attr('value', data));
	    //send request
	    form.appendTo('body').submit().remove();
	    $('#returnedJson').html("");
	};

	function getMainUrl(){
		$('#errorMessage').addClass("hide");
		var melData = 'melData.php?searchq=' + encodeURI($('#searchq').val()) +
					  '&maxRequestCount=' + $('#maxrequestcount').val();
		if ($('#searchFromDate').val())
		{
			var formattedsearchFromDate = formatDate($('#searchFromDate').val());
			melData = melData + "&fromDate=" + encodeURI(formattedsearchFromDate);
		}
		if ($('#searchToDate').val())
		{
			var formattedsearchToDate = formatDate($('#searchToDate').val());
			melData = melData + "&toDate=" + encodeURI(formattedsearchToDate);
		}
		$('#returnedJson').html("Getting twitter data...");

		return melData;

	}

	function formatDate(formatDate){
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
		search : sendSearch,
		export: sendExport
	};
})();
