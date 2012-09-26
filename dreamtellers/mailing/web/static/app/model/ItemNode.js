Ext.define('WebMailing.model.ItemNode', {
    extend: 'WebMailing.model.Item',
    requires: [
        'WebMailing.model.Item'
    ],
    fields: ["record"],
    proxy: {type:'memory'}
});
