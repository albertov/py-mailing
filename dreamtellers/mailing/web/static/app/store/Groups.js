Ext.define('WebMailing.store.Groups', {
    extend: 'Ext.data.Store',
    requires: 'WebMailing.model.Group',
    model: 'WebMailing.model.Group',
    remoteSort: true,
    buffered: true,
    pageSize: 100,
    sorters: [{
        property: 'name',
        direction: 'ASC'
    }],
    
});
