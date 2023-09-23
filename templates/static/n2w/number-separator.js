$(document).ready(function() {
    var commaCounter = 10;

    function numberSeparator(Number) {
        Number += '';
        for (var i = 0; i < commaCounter; i++) {
            Number = Number.replace(',', '');
        }
        x = Number.split('.');
        y = x[0];
        z = x.length > 1 ? '.' + x[1] : '';
        var rgx = /(\d+)(\d{3})/;
        while (rgx.test(y)) {
            y = y.replace(rgx, '$1' + ',' + '$2');
        }
        commaCounter++;
        return y + z;
    }
    $(document).on('keypress , paste , input', '.number-separator', function(e) {
        if (/.*/.test(e.key)) {
            $('.number-separator').on('input', function() {
                e.target.value = numberSeparator(e.target.value);
            });
        } else {
            e.preventDefault();
            return false;
        }
    });
})
// ^-?\d*[,.]?(\d{0,3},)*(\d{3},)?\d{0,3}$