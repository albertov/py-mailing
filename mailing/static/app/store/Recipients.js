Ext.define('Mailing.store.Recipients', {
    extend: 'Ext.data.Store',
    requires: 'Mailing.model.Recipient',
    model: 'Mailing.model.Recipient',
    remoteSort: true,
    buffered: true,
    pageSize: 100,
    autoSync: true,
    sorters: [{
        property: 'name',
        direction: 'ASC'
    }],
    
});
