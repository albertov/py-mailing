Ext.define('Mailing.store.Groups', {
    extend: 'Ext.data.Store',
    requires: 'Mailing.model.Group',
    model: 'Mailing.model.Group',
    remoteSort: true,
    buffered: true,
    autoSync: true,
    pageSize: 100,
    sorters: [{
        property: 'priority',
        direction: 'ASC'
    }],
    
});
