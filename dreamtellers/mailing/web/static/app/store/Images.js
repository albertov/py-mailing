Ext.define('WebMailing.store.Images', {
    extend: 'Ext.data.Store',
    requires: 'WebMailing.model.Image',
    model: 'WebMailing.model.Image',
    remoteSort: true,
    buffered: true,
    pageSize: 100,
    sorters: [{
        property: 'title',
        direction: 'ASC'
    }],
    
});
