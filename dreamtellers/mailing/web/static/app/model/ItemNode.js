Ext.define('WebMailing.model.ItemNode', {
    extend: 'WebMailing.model.Item',
    requires: [
        'WebMailing.model.Item'
    ],
    proxy: {type:'rest', url:'dummy'}
});
