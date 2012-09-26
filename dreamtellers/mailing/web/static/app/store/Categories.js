Ext.define('WebMailing.store.Categories', {
    extend: 'Ext.data.TreeStore',
    requires: 'WebMailing.model.Category',
    model: 'WebMailing.model.Category',
    remoteSort: true,
    autoLoad: true,
    autoSync: true,
    listeners: {
        write: function(store) {store.reload()}
    },
    rootProperty: 'categories',
    defaultRootProperty: 'categories'
});
