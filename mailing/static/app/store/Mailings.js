Ext.define('Mailing.store.Mailings', {
    extend: 'Ext.data.Store',
    requires: 'Mailing.model.Mailing',
    model: 'Mailing.model.Mailing',
    remoteSort: true,
    autoSync: true,
    autoLoad: true,
    buffered: true,
    pageSize: 100,
    sorters: [{
        property: 'number',
        direction: 'DESC'
    }],
    
});
