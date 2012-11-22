Ext.define('WebMailing.store.Mailings', {
    extend: 'Ext.data.Store',
    requires: 'WebMailing.model.Mailing',
    model: 'WebMailing.model.Mailing',
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
