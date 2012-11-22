Ext.define('WebMailing.store.Images', {
    extend: 'Ext.data.Store',
    requires: 'WebMailing.model.Image',
    model: 'WebMailing.model.Image',
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
