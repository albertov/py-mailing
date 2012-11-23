Ext.define('Mailing.Util', {
    singleton: true,
    renderBool: function(val) {
        var base = url('static/extjs/resources/themes/images/default/menu/'),
            yes = base + 'checked.gif',
            no = base + 'unchecked.gif',
            cb = ''
            + '<div style="text-align:center;height:13px;overflow:visible">'
            + '<img style="vertical-align:-3px" src="'
            + (val ? yes : no)
            + '"'
            + ' />'
            + '</div>'
        ;
        return cb;
    },
    renderError: function(val) {
        var base = url('static/extjs/resources/themes/images/default/tree/'),
            yes = base + 'drop-no.gif',
            no = base + 'drop-yes.gif',
            cb = ''
            + '<div style="text-align:center;height:13px;overflow:visible">'
            + '<img style="vertical-align:-3px" src="'
            + (val ? yes : no)
            + '"'
            + ' />'
            + '</div>'
        ;
        return cb;
    }
});
