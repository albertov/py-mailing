Ext.define('Mailing.store.Images', {
    extend: 'Ext.data.Store',
    requires: 'Mailing.model.Image',
    model: 'Mailing.model.Image',
    remoteSort: true,
    remoteFilter: true,
    buffered: true,
    autoSync: true,
    pageSize: 100,
    sorters: [{
        property: 'title',
        direction: 'ASC'
    }],
    
});
