Ext.define('Mailing.Rest', {
    extend: 'Ext.data.proxy.Rest',
    requires: 'Ext.window.MessageBox',
    alias: 'proxy.rest2',
    writer: {
        type: 'json',
        writeAllFields: false
    },
    listeners: {
        exception: function(proxy, response, operation) {
            if (response.status==400) {
                var record = operation.records[0];
                var resp = Ext.decode(response.responseText);
                var errors = [];
                for (var k in resp.errors) {
                    errors.push({
                        field: k,
                        value: record.get(k),
                        error: resp.errors[k]
                    });
                }
                var msg = (Ext.isEmpty(errors)?
                    resp.message : proxy.tpl.apply(errors));
                Ext.MessageBox.show({
                    title: "Error del servidor", // i18n
                    msg: msg,
                    icon: Ext.MessageBox.ERROR,
                    buttons: Ext.Msg.OK
                });
            } else {
                var e = operation.getError();
                Ext.MessageBox.show({
                    title: "Error desconocido del servidor", // i18n
                    msg: Ext.String.format("{0}: {1}", e.status, e.statusText),
                    icon: Ext.MessageBox.ERROR,
                    buttons: Ext.Msg.OK
                });
            }
        }
    },
    tpl: new Ext.XTemplate(
        '<h1>Errores</h1>',
        '<ul>',
        '<tpl for=".">',
            '<li>',
                '<dl>',
                    '<dt>Campo: {field}</dt>',
                    '<dd>{error}</dd>',
                '</dl>',
             '</li>',
         '</tpl>',
         '</ul>'
     )
});
