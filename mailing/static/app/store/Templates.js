Ext.define('Mailing.store.Templates', {
    extend: 'Ext.data.Store',
    requires: 'Mailing.model.Template',
    model: 'Mailing.model.Template',
    remoteSort: true,
    buffered: true,
    autoSync: true,
    pageSize: 100,
    sorters: [{
        property: 'title',
        direction: 'ASC'
    }],
    
});
