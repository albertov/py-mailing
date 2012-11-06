Ext.define('WebMailing.Rest', {
    extend: 'Ext.data.proxy.Rest',
    requires: 'Ext.window.MessageBox',
    alias: 'proxy.rest2',
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
                Ext.MessageBox.show({
                    title: "Error de validación del servidor", // i18n
                    msg: proxy.tpl.apply(errors),
                    icon: Ext.MessageBox.ERROR,
                    buttons: Ext.Msg.OK
                });
            } else {
                Ext.MessageBox.show({
                    title: "Error desconocido del servidor", // i18n
                    msg: operation.getError(),
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
                    '<dt>Campo:</dt>',
                    '<dd>{field}</dd>',
                    '<dt>Valor actual:</dt>',
                    '<dd>{value}</dd>',
                    '<dt>Error:</dt>',
                    '<dd>{error}</dd>',
                '</dl>',
             '</li>',
         '</tpl>',
         '</ul>'
     )
});
