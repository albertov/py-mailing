Ext.define('WebMailing.store.Recipients', {
    extend: 'Ext.data.Store',
    requires: 'WebMailing.model.Recipient',
    model: 'WebMailing.model.Recipient',
    remoteSort: true,
    buffered: true,
    pageSize: 100,
    autoSync: true,
    sorters: [{
        property: 'name',
        direction: 'ASC'
    }],
    
});
