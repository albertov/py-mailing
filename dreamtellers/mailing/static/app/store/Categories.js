Ext.define('WebMailing.store.Categories', {
    extend: 'Ext.data.TreeStore',
    requires: 'WebMailing.model.Category',
    model: 'WebMailing.model.Category',
    remoteSort: true,
    autoLoad: true,
    autoSync: true,
    rootProperty: 'categories',
    defaultRootProperty: 'categories',
    root: {
        title: 'Categorías', // i18n
        expanded: true
    }
});
