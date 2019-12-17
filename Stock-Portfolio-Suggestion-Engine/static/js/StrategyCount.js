function KeepCount() {
	var NewCount = 0;
	if (document.strategy.ethical.checked){ NewCount = NewCount + 1; }
	if (document.strategy.growth.checked){ NewCount = NewCount + 1; }
	if (document.strategy.index.checked){ NewCount = NewCount + 1; }
	if (document.strategy.quality.checked){ NewCount = NewCount + 1; }
	if (document.strategy.value.checked){ NewCount = NewCount + 1; }
	if (NewCount == 3){
		alert('You can only pick at most two strategies!')
		document.strategy; return false;
	}
	console.log("KeepCount");
}