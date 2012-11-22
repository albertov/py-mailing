Ext.define('Mailing.store.Categories', {
    extend: 'Ext.data.TreeStore',
    requires: 'Mailing.model.Category',
    model: 'Mailing.model.Category',
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
